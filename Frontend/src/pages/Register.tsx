import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/Button';
import { Header } from '../components/layout/Header';
import { authService } from '../services/api';

export const Register = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirm, setConfirm] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleRegister = async () => {
    if (password !== confirm) {
      setError('Passwords do not match');
      return;
    }

    try {
      await authService.register(email, password);
      navigate('/login');
    } catch (err: any) {
      setError(err.message || 'Registration failed');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white">
      <Header />
      <div className="flex flex-col items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="w-full max-w-md space-y-6 bg-white dark:bg-gray-800 p-8 rounded shadow">
          <h2 className="text-center text-2xl font-bold">Register for TeamLink</h2>

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
          <input
            type="password"
            value={confirm}
            onChange={(e) => setConfirm(e.target.value)}
            placeholder="Confirm Password"
            className="w-full p-2 rounded border border-gray-300 dark:border-gray-600 dark:bg-gray-700"
          />
          {error && <p className="text-red-500 text-sm">{error}</p>}

          <Button onClick={handleRegister} className="w-full">Register</Button>

          <p className="text-center text-sm text-gray-600 dark:text-gray-400">
            Already have an account?{' '}
            <button onClick={() => navigate('/login')} className="text-blue-500 hover:underline">
              Login
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};
