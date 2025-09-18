

import { Stack } from "expo-router";
import { useState } from "react";
import SplashScreen from "../components/SplashScreen";
import WelcomeScreen from "../components/WelcomeScreen";

export default function RootLayout() {
  const [showSplash, setShowSplash] = useState(true);
  const [showWelcome, setShowWelcome] = useState(false);

  if (showSplash) {
    return <SplashScreen onAnimationEnd={() => {
      setShowSplash(false);
      setShowWelcome(true);
    }} />;
  }

  if (showWelcome) {
    return <WelcomeScreen onDone={() => setShowWelcome(false)} />;
  }

  return <Stack screenOptions={{ headerShown: false }} />;
}
