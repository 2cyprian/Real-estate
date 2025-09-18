import React, { useState } from 'react';
import { Dimensions, Image, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { Colors } from '../constants/colors';

const { width } = Dimensions.get('window');

const introScreens = [
  {
    collage: [
      require("../assets/images/revenue-i1.png"),
      require("../assets/images/stock5.jpg"),
         ],
    title: "Karibu kwenye PropFinder!",
    desc: "Tafuta nyumba za kupanga kwa urahisi na haraka. Kuanzia vyumba vidogo hadi nyumba kubwa – zote zipo karibu nawe.",
  },
  {
    img: require("../assets/images/stock3.jpg"),
    title: "Kuama sio shida tena!",
    desc: "Acha stress za kutembea mtaa kwa mtaa. PropFinder inakuunganisha moja kwa moja na nyumba zinazokufaa.",
  },
  {
    img: require("../assets/images/stock4.jpg"),
    title: "Pata, Chagua, Hama Leo 🏠",
    desc: "Chagua nyumba unayoipenda, ongea moja kwa moja na mwenye nyumba, kisha hama bila longolongo.",
  },
];

export default function IntroSlider({ onDone }) {
  const [index, setIndex] = useState(0);
  const isLast = index === introScreens.length - 1;

  const handleNext = () => {
    if (isLast) {
      onDone && onDone();
    } else {
      setIndex(index + 1);
    }
  };

  const handlePrev = () => {
    if (index > 0) setIndex(index - 1);
  };

  const { collage, img, title, desc } = introScreens[index];

  return (
    <View style={styles.container}>
      {collage ? (
        <View style={styles.collageContainer}>
          <View style={{ flex: 1 }}>
            <Image
              source={collage[0]}
              style={[styles.collageLargeImg, { position: 'absolute', top: 0, right: 0, zIndex: 2 }]}
              resizeMode="cover"
            />
            <Image
              source={collage[1]}
              style={[
                styles.collageSmallImg,
                {
                  position: 'absolute',
                  left: 0,
                  bottom: 0,
                  zIndex: 3,
                  // Overlap upwards
                  transform: [{ translateY: 30 }],
                },
              ]}
              resizeMode="cover"
            />
          </View>
        </View>
      ) : (
        <Image source={img} style={styles.illustration} resizeMode="contain" />
      )}
      <Text style={styles.heading}>{title}</Text>
      <Text style={styles.body}>{desc}</Text>
      <View style={styles.dotsContainer}>
        {introScreens.map((_, i) => (
          <View key={i} style={[styles.dot, i === index && styles.activeDot]} />
        ))}
      </View>
      <View style={styles.buttonRow}>
        <TouchableOpacity style={styles.navButton} onPress={handlePrev} disabled={index === 0}>
          <Text style={[styles.navButtonText, index === 0 && { opacity: 0.3 }]}>←</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.ctaButton} onPress={handleNext}>
          <Text style={styles.ctaButtonText}>{isLast ? 'Anza Kutafuta Nyumba' : '→'}</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 34,
  },
  illustration: {
    width: width * 1.2,
    height: 280,
    marginBottom:32,
    top: 0,
  },
  heading: {
    fontSize: 22,
    fontWeight: 'bold',
    marginBottom: 12,
    textAlign: 'center',
    paddingHorizontal: 8,
    color: Colors.text[0],
    marginTop: 16,
  },
  body: {
    fontSize: 16,
    color: '#444',
    textAlign: 'center',
    marginBottom: 16,
    justifyContent: 'center',
  },
  dotsContainer: {
    flexDirection: 'row',
    marginBottom: 24,
  },
  dot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: '#ccc',
    marginHorizontal: 4,
  },
  activeDot: {
    backgroundColor: Colors.secondary[0],
  },
  buttonRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 12,
    paddingBottom: 24,
    bottom: 0,
    
  },
  navButton: {
    padding: 12,
    marginRight: 16,
  },
  navButtonText: {
    fontSize: 30,
        fontWeight: 'bold',
    color: Colors.primary[0],
  },
  ctaButton: {
    backgroundColor: Colors.primary[0],
    borderRadius: 24,
    paddingVertical: 12,
    paddingHorizontal: 28,
    alignItems: 'center',
  },
  ctaButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  
  collageContainer: {
    width: width * 0.9,
    height: 400,
    alignSelf: 'center',
    marginBottom: 16,
    justifyContent: 'center',
    
  },
  collageLargeImg: {
    width: 280,
    height: 390,
    borderRadius: 16,
    borderWidth: 2,
    borderColor: '#fff',
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowRadius: 6,
    backgroundColor: '#eee',
  },
  collageSmallImg: {
    width: 140,
    height: 150,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: '#fff',
    shadowColor: '#000',
    shadowOpacity: 0.08,
    shadowRadius: 4,
    backgroundColor: '#eee',
  },
});
