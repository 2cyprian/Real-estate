// styles/auth.styles.js
import { Colors } from "../../constants/colors";
import { StyleSheet } from "react-native";

export const styles = StyleSheet.create({
  container: {
    flex: 1,
  backgroundColor: Colors.light.background,
    padding: 20,
    justifyContent: "center",
  },
  illustration: {
    height: 310,
    width: 300,
    resizeMode: "contain",
  },
  title: {
    fontSize: 32,
    fontWeight: "bold",
  color: Colors.text[0],
    marginVertical: 15,
    textAlign: "center",
  },
  input: {
  backgroundColor: Colors.light.background,
    borderRadius: 12,
    padding: 15,
    marginBottom: 16,
    borderWidth: 1,
  borderColor: Colors.primary[1],
    fontSize: 16,
  color: Colors.text[0],
  },
  errorInput: {
  borderColor: Colors.secondary[2],
  },
  button: {
  backgroundColor: Colors.primary[0],
    borderRadius: 12,
    padding: 16,
    alignItems: "center",
    marginTop: 10,
    marginBottom: 20,
  },
  buttonText: {
  color: Colors.light.background,
    fontSize: 18,
    fontWeight: "600",
  },
  footerContainer: {
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
    gap: 8,
  },
  footerText: {
  color: Colors.text[0],
    fontSize: 16,
  },
  linkText: {
  color: Colors.primary[0],
    fontSize: 16,
    fontWeight: "600",
  },
  verificationContainer: {
    flex: 1,
  backgroundColor: Colors.light.background,
    padding: 20,
    justifyContent: "center",
    alignItems: "center",
  },
  verificationTitle: {
    fontSize: 24,
    fontWeight: "bold",
  color: Colors.text[0],
    marginBottom: 20,
    textAlign: "center",
  },
  verificationInput: {
  backgroundColor: Colors.light.background,
    borderRadius: 12,
    padding: 15,
    marginBottom: 16,
    borderWidth: 1,
  borderColor: Colors.primary[1],
    fontSize: 16,
  color: Colors.text[0],
    width: "100%",
    textAlign: "center",
    letterSpacing: 2,
  },

  // 🔴 Error styles
  errorBox: {
    backgroundColor: "#FFE5E5",
    padding: 12,
    borderRadius: 8,
    borderLeftWidth: 4,
  borderLeftColor: Colors.secondary[2],
    marginBottom: 16,
    flexDirection: "row",
    alignItems: "center",
    width: "100%",
  },
  errorText: {
  color: Colors.text[0],
    marginLeft: 8,
    flex: 1,
    fontSize: 14,
  },
});
