from typing import Dict, Any, List, Optional, Tuple
from sqlmodel import Session
from .mcp_server import MCPServer
import json
import re
import asyncio
import nest_asyncio


class OpenAIAgent:
    """
    OpenAI Agents SDK agent that:
    - Parses natural language
    - Selects MCP tools
    - Chains tools when needed
    - Confirms actions in friendly language
    - Never touches DB directly (uses MCP server)
    """

    def __init__(self, db_session: Session):
        self.mcp_server = MCPServer(db_session)
        self.tool_definitions = {
            "add_task": {
                "description": "Add a new task for the user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The ID of the user"},
                        "title": {"type": "string", "description": "The title of the task"},
                        "description": {"type": "string", "description": "Optional description of the task"}
                    },
                    "required": ["user_id", "title"]
                }
            },
            "list_tasks": {
                "description": "List tasks for the user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The ID of the user"},
                        "status": {"type": "string", "description": "Optional status filter (pending, completed)"}
                    },
                    "required": ["user_id"]
                }
            },
            "complete_task": {
                "description": "Complete a task for the user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The ID of the user"},
                        "task_id": {"type": "string", "description": "The ID of the task to complete"},
                        "mark_complete": {"type": "boolean", "description": "Whether to mark as complete (true) or incomplete (false)", "default": True}
                    },
                    "required": ["user_id", "task_id"]
                }
            },
            "delete_task": {
                "description": "Delete a task for the user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The ID of the user"},
                        "task_id": {"type": "string", "description": "The ID of the task to delete"}
                    },
                    "required": ["user_id", "task_id"]
                }
            },
            "update_task": {
                "description": "Update a task for the user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The ID of the user"},
                        "task_id": {"type": "string", "description": "The ID of the task to update"},
                        "title": {"type": "string", "description": "Optional new title"},
                        "description": {"type": "string", "description": "Optional new description"}
                    },
                    "required": ["user_id", "task_id"]
                }
            }
        }

    def parse_natural_language(self, text: str) -> List[Dict[str, Any]]:
        """
        Parse natural language to identify tool calls and extract parameters
        """
        text_lower = text.lower().strip()
        tool_calls = []

        # Pattern matching for different intents
        if self._is_add_task_intent(text_lower):
            title, description = self._extract_task_details(text)
            if title:
                tool_calls.append({
                    "name": "add_task",
                    "arguments": {"title": title, "description": description or ""}
                })

        elif self._is_list_tasks_intent(text_lower):
            status_filter = self._extract_status_filter(text_lower)
            tool_calls.append({
                "name": "list_tasks",
                "arguments": {"status": status_filter} if status_filter else {}
            })

        elif self._is_complete_task_intent(text_lower):
            task_id = self._extract_task_id(text_lower)
            title, _ = self._extract_task_details(text)
            
            args = {}
            if task_id:
                args["task_id"] = task_id
            elif title and title.lower() not in ["a", "an", "the", "it", "that", "this"]:
                # If no ID is found but we have a title, store the title for later resolution
                args["title"] = title
            
            # Check if the user wants to mark as incomplete (un-complete)
            text_lower = text.lower()
            if any(phrase in text_lower for phrase in ['un complete', 'uncomplete', 'mark un', 'mark as incomplete', 'not done', 'not finished', 'incomplete']):
                args["mark_complete"] = False
            else:
                args["mark_complete"] = True
            
            if args:  # Only add the tool call if we have some identifying information
                tool_calls.append({
                    "name": "complete_task",
                    "arguments": args
                })

        elif self._is_delete_task_intent(text_lower):
            task_id = self._extract_task_id(text_lower)
            title, _ = self._extract_task_details(text)
            
            args = {}
            if task_id:
                args["task_id"] = task_id
            elif title and title.lower() not in ["a", "an", "the", "it", "that", "this"]:
                # If no ID is found but we have a title, store the title for later resolution
                args["title"] = title
            
            if args:  # Only add the tool call if we have some identifying information
                tool_calls.append({
                    "name": "delete_task",
                    "arguments": args
                })

        elif self._is_update_task_intent(text_lower):
            task_id = self._extract_task_id(text_lower)
            title, description = self._extract_task_details(text)
            
            args = {}
            if task_id:
                args["task_id"] = task_id
            elif title and title.lower() not in ["a", "an", "the", "it", "that", "this"]:
                # If no ID is found but we have a title, store the title for later resolution
                args["task_title"] = title  # Use task_title to distinguish from update title
            
            if title or description:
                if title:
                    args["title"] = title
                if description:
                    args["description"] = description
            
            if "task_id" in args or "task_title" in args:  # Only add if we have identifying info
                tool_calls.append({
                    "name": "update_task",
                    "arguments": args
                })

        return tool_calls

    def _is_add_task_intent(self, text: str) -> bool:
        """Check if the text indicates an add task intent"""
        # Remove common prefixes that shouldn't affect intent detection
        text_clean = re.sub(r'^(please|pls|just|now|hey)\s+', '', text, flags=re.IGNORECASE)
        # Also remove common question starters like "can you", "could you", "would you"
        text_clean = re.sub(r'^(can|could|would|will)\s+(you|u)\s+', '', text_clean, flags=re.IGNORECASE)

        add_patterns = [
            r'\b(add|create|make|new|put|set)\b.*\b(a\s+)?(task|todo|item|thing|work|job)\b',
            r'\b(task|todo|item|thing|work|job)\b.*\b(add|create|make|new|put|set)\b',
            r'\bneed to\b.*\bdo\b',
            r'\bwant to\b.*\bdo\b',
            r'\bi should\b.*\bdo\b',
            r'\badd\b.*\b(to|for)\b',
            r'\b(add|create|make)\b.*\b(me|us|them)\b',
            r'\b(add|create|make)\b.*\ba\b.*\b(task|todo|item)\b'
        ]
        return any(re.search(pattern, text_clean, re.IGNORECASE) for pattern in add_patterns)

    def _is_list_tasks_intent(self, text: str) -> bool:
        """Check if the text indicates a list tasks intent"""
        # Remove common prefixes that shouldn't affect intent detection
        text_clean = re.sub(r'^(please|pls|just|now|hey)\s+', '', text, flags=re.IGNORECASE)

        list_patterns = [
            r'\b(list|show|display|see|view|get|fetch|retrieve)\b.*\b(task|todo|item|things|i have|to do|on my list)\b',
            r'\b(what|which)\b.*\b(todo|tasks|items|list)\b',
            r'\bmy\b.*\b(task|todo|list)\b',
            r'\bcheck\b.*\b(list|tasks)\b',
            r'\b(list|show|see|view)\b.*\bmy\b',
            r'\b(my|all)\b.*\b(task|todo|list)'
        ]
        return any(re.search(pattern, text_clean, re.IGNORECASE) for pattern in list_patterns)

    def _is_complete_task_intent(self, text: str) -> bool:
        """Check if the text indicates a complete task intent"""
        # Remove common prefixes that shouldn't affect intent detection
        text_clean = re.sub(r'^(please|pls|just|now|hey|can you|could you|will you|would you)\s+', '', text, flags=re.IGNORECASE)

        complete_patterns = [
            r'\b(complete|finish|done|mark as done|accomplish|achieve|tick off|check off)\b.*\b(task|todo|item)\b',
            r'\b(task|todo|item)\b.*\b(complete|finish|done|marked as done|accomplished|achieved|ticked off|checked off)\b',
            r'\bdone with\b.*\b(task|todo|item)\b',
            r'\bcomplete\b.*\bno\.\s*(\d+|\w+)',
            r'\bmark\b.*\b(as\s+)?(complete|done|finished)\b',
            r'\bfinish\b.*\b(task|todo|item)\b',
            r'\bmark\b.*\b(un\s+)?(complete|incomplete|not done|not finished)\b'  # Added for un-completing
        ]
        return any(re.search(pattern, text_clean, re.IGNORECASE) for pattern in complete_patterns)

    def _is_delete_task_intent(self, text: str) -> bool:
        """Check if the text indicates a delete task intent"""
        # Remove common prefixes that shouldn't affect intent detection
        text_clean = re.sub(r'^(please|pls|just|now|hey|can you|could you|will you|would you)\s+', '', text, flags=re.IGNORECASE)

        delete_patterns = [
            r'\b(delete|remove|eliminate|get rid of|cancel|trash|discard)\b.*\b(task|todo|item)\b',
            r'\b(task|todo|item)\b.*\b(delete|remove|eliminate|cancelled|trashed|discarded)\b',
            r'\bget rid of\b.*\b(task|todo|item)\b',
            r'\bremove\b.*\b(task|todo|item)\b'
        ]
        return any(re.search(pattern, text_clean, re.IGNORECASE) for pattern in delete_patterns)

    def _is_update_task_intent(self, text: str) -> bool:
        """Check if the text indicates an update task intent"""
        # Remove common prefixes that shouldn't affect intent detection
        text_clean = re.sub(r'^(please|pls|just|now|hey)\s+', '', text, flags=re.IGNORECASE)

        update_patterns = [
            r'\b(update|change|modify|edit|alter|revise)\b.*\b(task|todo|item)\b',
            r'\b(task|todo|item)\b.*\b(update|change|modify|edit|alter|revised)\b',
            r'\bchange\b.*\b(task|todo|item)\b',
            r'\bedit\b.*\b(task|todo|item)\b'
        ]
        return any(re.search(pattern, text_clean, re.IGNORECASE) for pattern in update_patterns)

    def _extract_task_details(self, text: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Extract task title and description from text
        """
        # Remove common prefixes like "add task", "please", etc.
        text_clean = re.sub(r'^(add|create|make|new|please|pls|can you|could you|just|now|hey|will you|would you)\s+', '', text, flags=re.IGNORECASE)
        # Remove "a task", "the task", "task", "a todo", "to do", etc. but keep the rest
        text_clean = re.sub(r'(a\s+)?(the\s+)?(task|todo|to\s+do|item|please|now)', '', text_clean, flags=re.IGNORECASE).strip()

        # Handle "for" and "to" patterns like "add a task for buy groceries" or "add task to buy groceries"
        # Look for content after "for" or "to"
        for_match = re.search(r'\b(for|to)\b\s*(.+)', text_clean, re.IGNORECASE)
        if for_match:
            extracted_text = for_match.group(2).strip()
            # Clean up common trailing words
            extracted_text = re.sub(r'\s+(please|now)$', '', extracted_text, flags=re.IGNORECASE)
            if len(extracted_text) > 3:
                return extracted_text, ""

        # Handle cases where the user says something like "add a task" without specifying what
        # If the cleaned text is empty or too generic, we'll return a default title
        if not text_clean or text_clean.lower() in ['a', 'an', 'the', 'me', 'it', 'something', 'anything']:
            return "Untitled task", "A task added via AI assistant"

        # Clean up punctuation and normalize
        text_clean = re.sub(r'[,:;]+', ' ', text_clean)
        text_clean = re.sub(r'\s+', ' ', text_clean).strip()

        # Try to extract title based on common patterns
        # Look for content in quotes first
        quote_match = re.search(r'["\'](.*?)["\']', text_clean)
        if quote_match:
            return quote_match.group(1).strip(), ""

        # If no quotes, use the first substantial phrase as title
        # Split by common conjunctions and take the first meaningful part
        parts = re.split(r'\s+(and|but|or|so|with|for|to|on|at)\s+', text_clean)
        title_candidate = parts[0].strip()

        # Only return as title if it's meaningful (not too short or generic)
        if len(title_candidate) > 3 and title_candidate.lower() not in ['the', 'a', 'an', 'my', 'our', 'this', 'that']:
            return title_candidate, ""

        # If we still don't have a good title, return a default
        if text_clean and len(text_clean) > 1:
            return text_clean, ""

        return "Untitled task", "A task added via AI assistant"

    def _extract_task_id(self, text: str) -> Optional[str]:
        """
        Extract task ID from text
        """
        # Look for numbers in the text that could represent task IDs
        number_matches = re.findall(r'\b(?:task\s+|#|no\.?\s*)?(\d+)\b', text, re.IGNORECASE)
        if number_matches:
            return number_matches[0]  # Return the first number found

        # Look for more complex patterns
        word_number_matches = re.findall(r'\b(task|item)\s+(\d+)\b', text, re.IGNORECASE)
        if word_number_matches:
            return word_number_matches[0][1]  # Return the number part

        return None

    def _find_task_by_title(self, text: str, user_id: str, db_session: Session) -> Optional[str]:
        """
        Find a task ID by matching the title in the user's text against existing tasks
        """
        from sqlmodel import select
        from ..models.task import Task
        import uuid
        
        # Normalize user_id to UUID if it's a string
        try:
            user_uuid = user_id if isinstance(user_id, uuid.UUID) else uuid.UUID(user_id)
        except ValueError:
            # If it's already in proper UUID format as string, use it as is
            user_uuid = user_id

        # Get all tasks for the user
        statement = select(Task).where(Task.user_id == user_uuid)
        tasks = db_session.exec(statement).all()

        # Clean the input text to extract potential task titles
        text_lower = text.lower()
        
        # Remove common prefixes that shouldn't be part of the task title
        text_clean = re.sub(r'^(please|pls|just|now|hey|can you|could you|delete|remove|complete|finish|done with|mark as|mark)\s+', '', text_lower, flags=re.IGNORECASE)
        
        # First, try exact matches or close matches with quotes
        # Look for quoted text in the original text which often indicates exact titles
        quoted_matches = re.findall(r'["\']([^"\']+)["\']', text)
        if quoted_matches:
            search_title = quoted_matches[0].lower().strip()
            # Try multiple variations of the search title to handle special characters
            search_variations = [
                search_title,  # Original
                re.sub(r'[^\w\s]', ' ', search_title),  # Replace special chars with spaces
                re.sub(r'[^\w\s]', '', search_title),  # Remove special chars completely
                re.sub(r'\s+', ' ', search_title).strip(),  # Normalize whitespace
            ]
            
            for variation in search_variations:
                variation_clean = re.sub(r'\s+', ' ', variation.strip())
                for task in tasks:
                    task_variations = [
                        task.title.lower(),  # Original
                        re.sub(r'[^\w\s]', ' ', task.title.lower()),  # Replace special chars with spaces
                        re.sub(r'[^\w\s]', '', task.title.lower()),  # Remove special chars completely
                        re.sub(r'\s+', ' ', task.title.lower()).strip(),  # Normalize whitespace
                    ]
                    
                    for task_variation in task_variations:
                        task_variation_clean = re.sub(r'\s+', ' ', task_variation.strip())
                        if variation_clean == task_variation_clean:
                            return str(task.id)
                        # Partial match check
                        if variation_clean in task_variation_clean or task_variation_clean in variation_clean:
                            return str(task.id)

        # If no quoted text, try to match based on the cleaned text
        # Look for task titles that match the cleaned text
        text_variations = [
            text_clean,
            re.sub(r'[^\w\s]', ' ', text_clean),  # Replace special chars with spaces
            re.sub(r'[^\w\s]', '', text_clean),  # Remove special chars completely
            re.sub(r'\s+', ' ', text_clean).strip(),  # Normalize whitespace
        ]
        
        for text_variation in text_variations:
            text_variation_clean = re.sub(r'\s+', ' ', text_variation.strip())
            for task in tasks:
                task_variations = [
                    task.title.lower(),  # Original
                    re.sub(r'[^\w\s]', ' ', task.title.lower()),  # Replace special chars with spaces
                    re.sub(r'[^\w\s]', '', task.title.lower()),  # Remove special chars completely
                    re.sub(r'\s+', ' ', task.title.lower()).strip(),  # Normalize whitespace
                ]
                
                for task_variation in task_variations:
                    task_variation_clean = re.sub(r'\s+', ' ', task_variation.strip())
                    # Check for exact match first
                    if task_variation_clean == text_variation_clean:
                        return str(task.id)
                    # Then check if the task title is contained in the text or vice versa
                    # Use a more precise matching approach
                    if text_variation_clean in task_variation_clean:
                        return str(task.id)
                    elif task_variation_clean in text_variation_clean:
                        # If the task title is in the text, check if it's a significant portion
                        if len(task_variation_clean) / len(text_variation_clean) > 0.5:  # At least 50% match
                            return str(task.id)

        return None

    def _extract_status_filter(self, text: str) -> Optional[str]:
        """
        Extract status filter from text
        """
        if 'completed' in text or 'done' in text or 'finished' in text:
            return 'completed'
        elif 'pending' in text or 'not done' in text or 'not finished' in text or 'todo' in text:
            return 'pending'
        return None

    async def execute_tool_chain(self, user_id: str, tool_calls: List[Dict[str, Any]], db_session: Session) -> List[Dict[str, Any]]:
        """
        Execute a chain of tool calls with proper user_id injection and task ID resolution
        """
        results = []

        for tool_call in tool_calls:
            tool_name = tool_call["name"]
            arguments = tool_call["arguments"].copy()  # Copy to avoid modifying original

            # Inject user_id into arguments for all tool calls
            arguments["user_id"] = user_id

            # For certain operations, if no task_id is provided, try to find it by title
            if tool_name in ["complete_task", "delete_task", "update_task"] and not arguments.get("task_id"):
                if "title" in arguments or "task_title" in arguments:
                    # If a title was provided, try to find the task by title
                    search_title = arguments.get("title") or arguments.get("task_title", "")
                    task_id = self._find_task_by_title(search_title, user_id, db_session)
                    if task_id:
                        arguments["task_id"] = task_id
                    else:
                        # If we couldn't find the task, return an error
                        results.append({
                            "tool_call": tool_call,
                            "result": {
                                "error": f"Could not find task matching '{search_title}'. Please list your tasks first to see available tasks.",
                                "success": False
                            }
                        })
                        continue
                else:
                    # If no title or ID is provided, try to infer from the original message
                    # This would require passing the original message, so for now we'll return an error
                    results.append({
                        "tool_call": tool_call,
                        "result": {
                            "error": f"No task specified. Please list your tasks first or provide a specific task title.",
                            "success": False
                        }
                    })
                    continue

            try:
                # Execute the tool call
                result = await self.mcp_server.call_tool(tool_name, arguments)
                results.append({
                    "tool_call": tool_call,
                    "result": result
                })
            except Exception as e:
                import traceback
                error_traceback = traceback.format_exc()
                print(f"Error executing tool {tool_name}: {str(e)}")
                print(f"Traceback: {error_traceback}")

                # Add error result
                results.append({
                    "tool_call": tool_call,
                    "result": {
                        "error": f"Failed to execute {tool_name}: {str(e)}",
                        "success": False
                    }
                })

        return results

    def generate_friendly_confirmation(self, tool_calls: List[Dict[str, Any]], results: List[Dict[str, Any]]) -> str:
        """
        Generate a friendly confirmation message based on tool calls and results
        """
        if not tool_calls:
            return "I understood your request, but I wasn't sure which action to take. Could you please be more specific?"

        confirmations = []
        for i, (tool_call, result_data) in enumerate(zip(tool_calls, results)):
            tool_name = tool_call["name"]
            result = result_data["result"]

            if not result.get("success"):
                error_msg = result.get("error", "Unknown error")
                confirmations.append(f"Sorry, I couldn't {tool_name.replace('_', ' ')}: {error_msg}")
                continue

            result_value = result.get("result", {})

            if tool_name == "add_task":
                title = result_value.get("title", "unnamed task")
                confirmations.append(f"I've added the task '{title}' to your list!")

            elif tool_name == "list_tasks":
                tasks = result_value.get("tasks", [])
                if not tasks:
                    confirmations.append("You don't have any tasks on your list.")
                else:
                    total = result_value.get("total_count", len(tasks))
                    status_filter = result_value.get("filters_applied", {}).get("status")
                    if status_filter:
                        confirmations.append(f"You have {total} {status_filter} tasks:")
                        for j, task in enumerate(tasks[:3]):  # Show first 3 tasks
                            confirmations.append(f"  - {task.get('title', 'Unnamed task')}")
                        if len(tasks) > 3:
                            confirmations.append(f"  ... and {len(tasks) - 3} more")
                    else:
                        confirmations.append(f"You have {total} tasks in total. Here are a few:")
                        for j, task in enumerate(tasks[:3]):  # Show first 3 tasks
                            status = task.get('status', 'unknown')
                            confirmations.append(f"  - {task.get('title', 'Unnamed task')} ({status})")
                        if len(tasks) > 3:
                            confirmations.append(f"  ... and {len(tasks) - 3} more")

            elif tool_name == "complete_task":
                task_title = result_value.get("title", "the task")
                is_completed = result_value.get("is_completed", True)
                if is_completed:
                    confirmations.append(f"I've marked '{task_title}' as completed!")
                else:
                    confirmations.append(f"I've marked '{task_title}' as incomplete!")

            elif tool_name == "delete_task":
                confirmations.append("I've deleted the task from your list.")

            elif tool_name == "update_task":
                task_title = result_value.get("title", "the task")
                confirmations.append(f"I've updated the task to '{task_title}'.")

        return " ".join(confirmations)

    async def process_request(self, user_id: str, message: str, db_session) -> Dict[str, Any]:
        """
        Process a user request using natural language parsing and MCP tools
        Following the required flow:
        1. Parse natural language to identify intent
        2. Select appropriate MCP tools
        3. Execute tool chain
        4. Capture results
        5. Generate friendly response
        """
        try:
            # Parse the natural language message (step 3: Run agent -> sub-step 1)
            tool_calls = self.parse_natural_language(message)

            # Execute the tool chain (step 3: Run agent -> sub-step 2 & 4: Capture MCP tool calls)
            if tool_calls:
                results = await self.execute_tool_chain(user_id, tool_calls, db_session)
                confirmation = self.generate_friendly_confirmation(tool_calls, results)
            else:
                # If no tools were identified, provide a helpful response
                confirmation = "I'm not sure what you'd like me to do. I can help you add, list, complete, delete, or update tasks. Could you please be more specific."
                results = []

            # Return data for steps 5 & 6: Store and return response
            return {
                "response": confirmation,
                "tool_calls_executed": len(tool_calls),
                "tool_calls": tool_calls,  # Captured tool calls for return
                "results": results
            }
        except Exception as e:
            import traceback
            error_traceback = traceback.format_exc()
            print(f"Error in process_request: {str(e)}")
            print(f"Traceback: {error_traceback}")

            # Return an error response
            return {
                "response": "Sorry, I encountered an error processing your request.",
                "tool_calls_executed": 0,
                "tool_calls": [],
                "results": []
            }


# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()