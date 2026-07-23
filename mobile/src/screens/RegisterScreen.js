import { useState } from 'react';
import {
  Text,
  TextInput,
  Pressable,
  StyleSheet,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
} from 'react-native';
import { useAuth } from '../context/AuthContext';

export default function RegisterScreen({ navigation }) {
  const { register } = useAuth();
  const [form, setForm] = useState({
    username: '',
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const setField = (key) => (value) => setForm((prev) => ({ ...prev, [key]: value }));

  const handleRegister = async () => {
    if (!form.username.trim() || !form.password) {
      setError("Login va parolni to'ldiring");
      return;
    }
    if (form.password !== form.confirmPassword) {
      setError('Parollar mos kelmadi');
      return;
    }

    setError('');
    setLoading(true);
    const result = await register({
      username: form.username.trim(),
      password: form.password,
      email: form.email.trim(),
      first_name: form.first_name.trim(),
      last_name: form.last_name.trim(),
    });
    setLoading(false);

    if (!result.success) setError(result.error);
  };

  return (
    <KeyboardAvoidingView
      style={styles.flex}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <ScrollView contentContainerStyle={styles.container} keyboardShouldPersistTaps="handled">
        <Text style={styles.title}>Ro'yxatdan o'tish</Text>
        <Text style={styles.subtitle}>Yangi hisob yarating</Text>

        <TextInput
          style={styles.input}
          placeholder="Login *"
          value={form.username}
          onChangeText={setField('username')}
          autoCapitalize="none"
          autoCorrect={false}
          editable={!loading}
        />
        <TextInput
          style={styles.input}
          placeholder="Ism"
          value={form.first_name}
          onChangeText={setField('first_name')}
          editable={!loading}
        />
        <TextInput
          style={styles.input}
          placeholder="Familiya"
          value={form.last_name}
          onChangeText={setField('last_name')}
          editable={!loading}
        />
        <TextInput
          style={styles.input}
          placeholder="Email"
          value={form.email}
          onChangeText={setField('email')}
          keyboardType="email-address"
          autoCapitalize="none"
          autoCorrect={false}
          editable={!loading}
        />
        <TextInput
          style={styles.input}
          placeholder="Parol *"
          value={form.password}
          onChangeText={setField('password')}
          secureTextEntry
          autoCapitalize="none"
          editable={!loading}
        />
        <TextInput
          style={styles.input}
          placeholder="Parolni tasdiqlang *"
          value={form.confirmPassword}
          onChangeText={setField('confirmPassword')}
          secureTextEntry
          autoCapitalize="none"
          editable={!loading}
          onSubmitEditing={handleRegister}
        />

        {error ? <Text style={styles.error}>{error}</Text> : null}

        <Pressable
          style={({ pressed }) => [styles.button, (pressed || loading) && styles.buttonPressed]}
          onPress={handleRegister}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.buttonText}>Ro'yxatdan o'tish</Text>
          )}
        </Pressable>

        <Pressable onPress={() => navigation.goBack()} disabled={loading}>
          <Text style={styles.link}>Hisobingiz bormi? Kirish</Text>
        </Pressable>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  flex: { flex: 1, backgroundColor: '#fff' },
  container: { flexGrow: 1, justifyContent: 'center', padding: 24, paddingVertical: 40 },
  title: { fontSize: 30, fontWeight: '700', color: '#111' },
  subtitle: { fontSize: 15, color: '#666', marginTop: 6, marginBottom: 28 },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 10,
    paddingHorizontal: 16,
    paddingVertical: 14,
    fontSize: 16,
    marginBottom: 14,
    backgroundColor: '#fafafa',
  },
  error: { color: '#d32f2f', marginBottom: 12, fontSize: 14 },
  button: {
    backgroundColor: '#e8590c',
    borderRadius: 10,
    paddingVertical: 16,
    alignItems: 'center',
    marginTop: 4,
  },
  buttonPressed: { opacity: 0.8 },
  buttonText: { color: '#fff', fontSize: 16, fontWeight: '600' },
  link: { color: '#e8590c', textAlign: 'center', marginTop: 20, fontSize: 15 },
});
