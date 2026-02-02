// Pakistan-inspired Color Palette
export const pakistanColors = {
  // Primary Pakistan Green
  primary: '#01411C',      // Official Pakistan green
  primaryDark: '#002800',  // Darker shade for depth
  primaryLight: '#006600', // Lighter shade for accents
  primaryAccent: '#00A651', // Brighter green for highlights

  // Secondary Colors
  secondary: '#FFFFFF',    // White (from Pakistan flag)
  secondaryDark: '#CCCCCC', // Darker white for contrast
  secondaryLight: '#F5F5F5', // Lighter for backgrounds

  // Accent Colors
  gold: '#FFBF00',         // Gold from Pakistan flag
  goldDark: '#CC9900',     // Darker gold
  goldLight: '#FFD700',    // Lighter gold

  // Dark Theme Colors
  background: '#121212',   // Deep charcoal
  surface: '#1e1e1e',      // Cards and surfaces
  surfaceLight: '#2d2d2d', // Lighter surfaces
  surfaceDark: '#0d0d0d',  // Darker surfaces

  // Text Colors
  textPrimary: '#ffffff',  // Main text on dark
  textSecondary: '#b0b0b0', // Secondary text
  textDisabled: '#666666', // Disabled text
  textOnPrimary: '#ffffff', // Text on primary color

  // Status Colors
  success: '#4CAF50',      // Green for success
  warning: '#FFC107',      // Amber for warnings
  error: '#F44336',        // Red for errors
  info: '#2196F3',         // Blue for info
  neutral: '#9E9E9E',      // Gray for neutral
};

// Export as CSS variables for use in stylesheets
export const cssVariables = {
  '--pak-primary': pakistanColors.primary,
  '--pak-primary-dark': pakistanColors.primaryDark,
  '--pak-primary-light': pakistanColors.primaryLight,
  '--pak-primary-accent': pakistanColors.primaryAccent,
  '--pak-secondary': pakistanColors.secondary,
  '--pak-gold': pakistanColors.gold,
  '--pak-background': pakistanColors.background,
  '--pak-surface': pakistanColors.surface,
  '--pak-text-primary': pakistanColors.textPrimary,
  '--pak-text-secondary': pakistanColors.textSecondary,
  '--pak-success': pakistanColors.success,
  '--pak-warning': pakistanColors.warning,
  '--pak-error': pakistanColors.error,
  '--pak-info': pakistanColors.info,
};

// Helper function to apply colors to DOM
export const applyColorsToDOM = () => {
  const root = document.documentElement;
  Object.entries(cssVariables).forEach(([property, value]) => {
    root.style.setProperty(property, value);
  });
};

// Export individual color palettes
export const darkTheme = {
  background: pakistanColors.background,
  surface: pakistanColors.surface,
  textPrimary: pakistanColors.textPrimary,
  textSecondary: pakistanColors.textSecondary,
  primary: pakistanColors.primary,
  secondary: pakistanColors.secondary,
  accent: pakistanColors.gold,
};

export const lightTheme = {
  background: pakistanColors.secondary,
  surface: pakistanColors.secondaryLight,
  textPrimary: pakistanColors.primary,
  textSecondary: pakistanColors.primaryLight,
  primary: pakistanColors.primary,
  secondary: pakistanColors.secondary,
  accent: pakistanColors.gold,
};