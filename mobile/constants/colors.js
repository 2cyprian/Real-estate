import { Platform } from 'react-native';

const tintColorLight = '#0a7ea4';
const tintColorDark = '#fff';

export const Colors = {
  primary: [
    '#2B5F74',
    '#688C9A',
    '#7D9BA8',
    '#8DA5B1',
    '#97A7AB',
  ],
  secondary: [
    '#E68A7C',
    '#F6BF88',
    '#CF6F65',
    
  ],
  text: [
    '#000000',
    '#444444',
    '#646464',
    '#858585',
    '#BBBBBB',
  ],
  light: {
    text: '#11181C',
    background: '#fff',
    tint: tintColorLight,
    icon: '#687076',
    tabIconDefault: '#687076',
    tabIconSelected: tintColorLight,
  },
  dark: {
    text: '#ECEDEE',
    background: '#151718',
    tint: tintColorDark,
    icon: '#9BA1A6',
    tabIconDefault: '#9BA1A6',
    tabIconSelected: tintColorDark,
  },
};

export const Fonts = Platform.select({
  ios: { sans: 'Gilroy', serif: 'Gilroy', rounded: 'Gilroy', mono: 'Gilroy' },
  android: { sans: 'Gilroy', serif: 'Gilroy', rounded: 'Gilroy', mono: 'Gilroy' },
  default: { sans: 'Gilroy', serif: 'Gilroy', rounded: 'Gilroy', mono: 'Gilroy' },
  web: {
    sans: "'Gilroy', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
    serif: "'Gilroy', Georgia, 'Times New Roman', serif",
    rounded: "'Gilroy', 'SF Pro Rounded', 'Hiragino Maru Gothic ProN', Meiryo, 'MS PGothic', sans-serif",
    mono: "'Gilroy', SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace",
  },
});
