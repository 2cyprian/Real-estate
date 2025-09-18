import { useEffect, useRef } from 'react';
import { Animated, StyleSheet, View } from 'react-native';

export default function SplashScreen({ onAnimationEnd }) {
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const scaleAnim = useRef(new Animated.Value(0.8)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 2200,
        useNativeDriver: true,
      }),
      Animated.spring(scaleAnim, {
        toValue: 1,
        friction: 4,
        useNativeDriver: true,
      }),
    ]).start(() => {
      if (onAnimationEnd) onAnimationEnd();
    });
  }, [fadeAnim, scaleAnim, onAnimationEnd]);

  return (
    <View style={styles.container}>
      <Animated.Image
        source={require('../assets/images/AppIcons/Assets.xcassets/AppIcon.appiconset/1024.png')}
        style={[
          styles.logo,
          {
            opacity: fadeAnim,
            transform: [{ scale: scaleAnim }],
          },
        ]}
        resizeMode="contain"
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  logo: {
    width: 180,
    height: 180,
  },
});
