import { SafeAreaView, ScrollView, StyleSheet, Text, TouchableOpacity, View } from 'react-native';

export default function Home() {
  return (
    <SafeAreaView style={styles.safe}>
      <ScrollView contentContainerStyle={styles.container}>
        <View style={styles.hero}>
          <Text style={styles.logo}>JobIA</Text>
          <Text style={styles.title}>Tu asistente inteligente de empleo</Text>
          <Text style={styles.subtitle}>Encuentra oportunidades según tu perfil y recibe alertas cuando aparezcan nuevas coincidencias.</Text>
        </View>

        <TouchableOpacity style={styles.primary}>
          <Text style={styles.primaryText}>🔎 Buscar oportunidades</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.card}>
          <Text style={styles.cardTitle}>👤 Mi perfil JobIA</Text>
          <Text style={styles.cardText}>Configura experiencia, habilidades, idiomas, ubicación y preferencias.</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.card}>
          <Text style={styles.cardTitle}>🔔 Alertas</Text>
          <Text style={styles.cardText}>Elige la frecuencia de búsqueda y recibe las oportunidades relevantes por correo.</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.card}>
          <Text style={styles.cardTitle}>📊 Comprobar estado</Text>
          <Text style={styles.cardText}>Consulta la última búsqueda y el estado de tus alertas.</Text>
        </TouchableOpacity>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: '#f7f9fc' },
  container: { padding: 22, gap: 14 },
  hero: { paddingVertical: 28 },
  logo: { fontSize: 38, fontWeight: '800', color: '#208AEF' },
  title: { fontSize: 27, fontWeight: '800', color: '#172033', marginTop: 8 },
  subtitle: { fontSize: 16, lineHeight: 24, color: '#5c667a', marginTop: 10 },
  primary: { backgroundColor: '#208AEF', borderRadius: 16, padding: 18, alignItems: 'center' },
  primaryText: { color: '#fff', fontSize: 17, fontWeight: '700' },
  card: { backgroundColor: '#fff', borderRadius: 16, padding: 18, borderWidth: 1, borderColor: '#e4e8ef' },
  cardTitle: { fontSize: 18, fontWeight: '700', color: '#172033' },
  cardText: { fontSize: 14, lineHeight: 21, color: '#667085', marginTop: 6 }
});
