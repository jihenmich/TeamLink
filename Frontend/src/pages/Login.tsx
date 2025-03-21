import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/Button';
import { useAuthStore } from '../store/auth';

export const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  const handleLogin = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          username: email,
          password: password,
        }),
      });

      if (!response.ok) {
        throw new Error('Invalid credentials');
      }

      const data = await response.json();
      useAuthStore.getState().setAccessToken(data.access_token);
      navigate('/dashboard');
    } catch (error) {
      setErrorMessage('Invalid email or password');
      console.error('Login failed:', error);
    }
  };

  const goToRegister = () => {
    navigate('/register');  // Navigiere zur Registrierungsseite
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h1 className="text-center text-3xl font-bold text-gray-900 mb-8">
          Welcome to TeamLink
        </h1>

        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <div className="space-y-6">
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Email"
              className="w-full p-2 border border-gray-300 rounded"
            />
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password"
              className="w-full p-2 border border-gray-300 rounded"
            />
            {errorMessage && (
              <div className="text-red-500 text-sm">{errorMessage}</div>
            )}
            <Button onClick={handleLogin} className="w-full">
              Login
            </Button>

            <div className="mt-4 text-center">
              <span className="text-sm text-gray-600">
                Don't have an account?{' '}
                <button
                  onClick={goToRegister}
                  className="text-blue-500 hover:text-blue-700"
                >
                  Register here
                </button>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
