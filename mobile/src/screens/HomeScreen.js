import { View, Text, Pressable, StyleSheet } from 'react-native';
import { useAuth } from '../context/AuthContext';

export default function HomeScreen() {
  const { user, logout } = useAuth();

  return (
    <View style={styles.container}>
      <Text style={styles.greeting}>
        Salom, {user?.first_name || user?.username}!
      </Text>
      <Text style={styles.meta}>Login: {user?.username}</Text>
      {user?.email ? <Text style={styles.meta}>Email: {user.email}</Text> : null}
      {user?.is_staff ? <Text style={styles.badge}>Admin</Text> : null}

      <Pressable
        style={({ pressed }) => [styles.button, pressed && styles.buttonPressed]}
        onPress={logout}
      >
        <Text style={styles.buttonText}>Chiqish</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff', padding: 24, justifyContent: 'center' },
  greeting: { fontSize: 26, fontWeight: '700', color: '#111', marginBottom: 16 },
  meta: { fontSize: 16, color: '#555', marginBottom: 6 },
  badge: {
    alignSelf: 'flex-start',
    marginTop: 8,
    backgroundColor: '#e8590c',
    color: '#fff',
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 20,
    fontSize: 13,
    fontWeight: '600',
  },
  button: {
    marginTop: 32,
    borderWidth: 1,
    borderColor: '#e8590c',
    borderRadius: 10,
    paddingVertical: 14,
    alignItems: 'center',
  },
  buttonPressed: { opacity: 0.7 },
  buttonText: { color: '#e8590c', fontSize: 16, fontWeight: '600' },
});
