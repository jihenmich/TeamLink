import create from 'zustand';
import api from '../services/api'; // dein Axios-Client mit Token-Header

interface AuthState {
  accessToken: string | null;
  isAuthenticated: boolean;
  user: { name: string } | null;
  setAccessToken: (token: string) => void;
  logout: () => void;
  fetchUser: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  accessToken: null,
  isAuthenticated: false,
  user: null,

  setAccessToken: (token: string) => {
    set({ accessToken: token, isAuthenticated: true });
    get().fetchUser();
  },

  logout: () => {
    set({ accessToken: null, isAuthenticated: false, user: null });
  },

  fetchUser: async () => {
    try {
      const response = await api.get('/auth/profile');
      set({ user: { name: response.data.name } });
    } catch (error) {
      console.error('Fehler beim Laden des Benutzerprofils:', error);
    }
  },
}));
