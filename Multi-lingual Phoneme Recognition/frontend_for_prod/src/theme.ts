'use client';
import { Roboto } from 'next/font/google';
import { createTheme } from '@mui/material/styles';
import { CssVarsProvider, extendTheme } from '@mui/material-next/styles';

const roboto = Roboto({
  weight: ['300', '400', '500', '700'],
  subsets: ['latin'],
  display: 'swap',
});

export const theme2 = createTheme({
  typography: {
    fontFamily: roboto.style.fontFamily,
  },
});

export const theme3 = extendTheme();