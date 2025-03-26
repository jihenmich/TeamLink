import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/Button';
import { useAuthStore } from '../store/auth';
import { authService } from '../services/api';
import { Header } from '../components/layout/Header';

export const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const res = await authService.login(email, password);
      useAuthStore.getState().setAccessToken(res.access_token);
      navigate('/dashboard');
    } catch {
      setError('Invalid email or password');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white">
      <Header />
      <div className="flex flex-col items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="w-full max-w-md space-y-6 bg-white dark:bg-gray-800 p-8 rounded shadow">
          <h2 className="text-center text-2xl font-bold">Welcome to TeamLink</h2>

          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Email"
            className="w-full p-2 rounded border border-gray-300 dark:border-gray-600 dark:bg-gray-700"
          />
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            className="w-full p-2 rounded border border-gray-300 dark:border-gray-600 dark:bg-gray-700"
          />
          {error && <p className="text-red-500 text-sm">{error}</p>}

          <Button onClick={handleLogin} className="w-full">Login</Button>

          <p className="text-center text-sm text-gray-600 dark:text-gray-400">
            Don't have an account?{' '}
            <button onClick={() => navigate('/register')} className="text-blue-500 hover:underline">
              Register
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};
