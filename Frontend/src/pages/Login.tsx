import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Github } from 'lucide-react';
import { Button } from '../components/ui/Button';
import { useAuthStore } from '../store/auth';

export const Login = () => {
  const navigate = useNavigate();
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/dashboard');
    }
  }, [isAuthenticated, navigate]);

  const handleLogin = () => {
    const clientId = import.meta.env.VITE_OAUTH_CLIENT_ID;
    const redirectUri = `${window.location.origin}/oauth/callback`;
    const scope = 'read:user user:email';
    
    window.location.href = `https://github.com/login/oauth/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&scope=${scope}`;
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h1 className="text-center text-3xl font-bold text-gray-900 mb-8">
          Welcome to TeamLink
        </h1>
        
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <div className="space-y-6">
            <Button
              onClick={handleLogin}
              className="w-full flex items-center justify-center space-x-2"
            >
              <Github className="w-5 h-5" />
              <span>Sign in with GitHub</span>
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};