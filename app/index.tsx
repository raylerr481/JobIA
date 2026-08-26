import { useState } from 'react';
import { SafeAreaView, ScrollView, StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native';

const professions = ['Informática / IT', 'Administración', 'Educación', 'Diseño', 'Marketing', 'Contabilidad', 'Oficios técnicos', 'Ventas', 'Salud', 'Otra'];
const modes = ['Remoto', 'Presencial', 'Híbrido'];
const frequencies = ['Cada pocas horas', 'Diario', 'Cada 2 días', 'Semanal', 'Pausado'];

export default function Home() {
  const [section, setSection] = useState<'home' | 'profile' | 'alerts' | 'search'>('home');
  const [profession, setProfession] = useState('');
  const [mode, setMode] = useState('Remoto');
  const [frequency, setFrequency] = useState('Diario');
  const [email, setEmail] = useState('');
  const [aiIncome, setAiIncome] = useState(false);

  if (section === 'profile') return <Screen title="👤 Mi perfil JobIA" onBack={() => setSection('home')}>
    <Text style={styles.label}>Correo electrónico</Text>
    <TextInput value={email} onChangeText={setEmail} placeholder="tu@email.com" keyboardType="email-address" style={styles.input} />
    <Text style={styles.label}>Profesión principal</Text>
    <View style={styles.wrap}>{professions.map(p => <Choice key={p} label={p} selected={profession === p} onPress={() => setProfession(p)} />)}</View>
    <Text style={styles.label}>Modalidad</Text>
    <View style={styles.wrap}>{modes.map(m => <Choice key={m} label={m} selected={mode === m} onPress={() => setMode(m)} />)}</View>
    <Choice label="🤖 Quiero oportunidades de IA / human-in-the-loop" selected={aiIncome} onPress={() => setAiIncome(!aiIncome)} />
    <Button label="Guardar perfil" onPress={() => setSection('home')} />
  </Screen>;

  if (section === 'alerts') return <Screen title="🔔 Alertas" onBack={() => setSection('home')}>
    <Text style={styles.label}>Frecuencia de búsqueda</Text>
    {frequencies.map(f => <Choice key={f} label={f} selected={frequency === f} onPress={() => setFrequency(f)} />)}
    <Text style={styles.muted}>Las búsquedas y alertas son individuales. No existe una rutina global obligatoria.</Text>
    <Button label="Guardar alertas" onPress={() => setSection('home')} />
  </Screen>;

  if (section === 'search') return <Screen title="🔎 Oportunidades" onBack={() => setSection('home')}>
    <View style={styles.result}><Text style={styles.score}>94% Match</Text><Text style={styles.resultTitle}>AI Response Evaluator</Text><Text style={styles.muted}>Remoto · Brasil · Human-in-the-loop</Text><Text style={styles.resultText}>Coincide con tu perfil por habilidades, modalidad y preferencias.</Text></View>
    <View style={styles.result}><Text style={styles.score}>89% Match</Text><Text style={styles.resultTitle}>Soporte técnico remoto</Text><Text style={styles.muted}>Remoto · Tiempo completo</Text><Text style={styles.resultText}>Experiencia IT y soporte técnico compatibles.</Text></View>
    <Text style={styles.muted}>Estas tarjetas son una vista inicial. Las oportunidades reales se conectarán al backend antes del lanzamiento.</Text>
  </Screen>;

  return <SafeAreaView style={styles.safe}><ScrollView contentContainerStyle={styles.container}>
    <Text style={styles.logo}>JobIA</Text><Text style={styles.title}>Tu asistente inteligente de empleo</Text>
    <Text style={styles.subtitle}>Encuentra trabajo y oportunidades de ingresos según lo que sabes hacer.</Text>
    <Button label="🔎 Buscar oportunidades" onPress={() => setSection('search')} />
    <Card title="👤 Mi perfil JobIA" text="Profesión, experiencia, habilidades, ubicación y preferencias." onPress={() => setSection('profile')} />
    <Card title="🔔 Alertas" text={`${frequency} · ${email || 'correo no configurado'}`} onPress={() => setSection('alerts')} />
    <Card title="🤖 Bitey Trainer" text="Oportunidades de entrenamiento, evaluación de IA y trabajo human-in-the-loop." onPress={() => setSection('search')} />
    <Card title="📊 Comprobar estado" text="Revisa tu última búsqueda y el estado de las alertas." onPress={() => setSection('alerts')} />
  </ScrollView></SafeAreaView>;
}

function Screen({ title, onBack, children }: { title: string; onBack: () => void; children: React.ReactNode }) { return <SafeAreaView style={styles.safe}><ScrollView contentContainerStyle={styles.container}><TouchableOpacity onPress={onBack}><Text style={styles.back}>← Volver</Text></TouchableOpacity><Text style={styles.screenTitle}>{title}</Text>{children}</ScrollView></SafeAreaView>; }
function Button({ label, onPress }: { label: string; onPress: () => void }) { return <TouchableOpacity style={styles.primary} onPress={onPress}><Text style={styles.primaryText}>{label}</Text></TouchableOpacity>; }
function Card({ title, text, onPress }: { title: string; text: string; onPress: () => void }) { return <TouchableOpacity style={styles.card} onPress={onPress}><Text style={styles.cardTitle}>{title}</Text><Text style={styles.cardText}>{text}</Text></TouchableOpacity>; }
function Choice({ label, selected, onPress }: { label: string; selected: boolean; onPress: () => void }) { return <TouchableOpacity style={[styles.choice, selected && styles.choiceSelected]} onPress={onPress}><Text style={styles.choiceText}>{selected ? '✓ ' : ''}{label}</Text></TouchableOpacity>; }

const styles = StyleSheet.create({ safe:{flex:1,backgroundColor:'#f7f9fc'},container:{padding:22,gap:14},logo:{fontSize:40,fontWeight:'800',color:'#208AEF'},title:{fontSize:27,fontWeight:'800',color:'#172033',marginTop:4},screenTitle:{fontSize:27,fontWeight:'800',color:'#172033',marginBottom:10},subtitle:{fontSize:16,lineHeight:24,color:'#5c667a',marginBottom:10},primary:{backgroundColor:'#208AEF',borderRadius:16,padding:18,alignItems:'center'},primaryText:{color:'#fff',fontSize:17,fontWeight:'700'},card:{backgroundColor:'#fff',borderRadius:16,padding:18,borderWidth:1,borderColor:'#e4e8ef'},cardTitle:{fontSize:18,fontWeight:'700',color:'#172033'},cardText:{fontSize:14,lineHeight:21,color:'#667085',marginTop:6},back:{color:'#208AEF',fontSize:16,fontWeight:'700',marginBottom:8},label:{fontSize:15,fontWeight:'700',color:'#172033',marginTop:8},input:{backgroundColor:'#fff',borderWidth:1,borderColor:'#d8dee8',borderRadius:12,padding:14,fontSize:16},wrap:{flexDirection:'row',flexWrap:'wrap',gap:8},choice:{backgroundColor:'#fff',borderWidth:1,borderColor:'#d8dee8',borderRadius:12,padding:12},choiceSelected:{borderColor:'#208AEF',backgroundColor:'#eef7ff'},choiceText:{color:'#172033',fontWeight:'600'},muted:{color:'#667085',lineHeight:21},result:{backgroundColor:'#fff',borderRadius:16,padding:18,borderWidth:1,borderColor:'#e4e8ef',gap:5},score:{color:'#208AEF',fontWeight:'800'},resultTitle:{fontSize:19,fontWeight:'800',color:'#172033'},resultText:{color:'#4b5565',lineHeight:21}}
