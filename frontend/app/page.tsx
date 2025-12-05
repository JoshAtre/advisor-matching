'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '../utils/api';

export default function Home() {
  const router = useRouter();
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      if (isLogin) {
        // Since OAuth2 expects form-data, we format it specifically
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);
        
        const res = await fetch('http://localhost:8000/token', {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: formData,
        });

        if (!res.ok) throw new Error('Invalid credentials');
        const data = await res.json();
        localStorage.setItem('token', data.access_token);
        router.push('/dashboard');
      } else {
        const res = await api.post('/signup', { email, password, full_name: fullName });
        if (!res.ok) throw new Error('Signup failed');
        // Auto login after signup
        setIsLogin(true);
        setError('Account created! Please log in.');
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full space-y-8 p-8 bg-white rounded shadow">
        <h2 className="text-center text-3xl font-extrabold text-gray-900">
          {isLogin ? 'Sign in to AdvisorMatch' : 'Create Account'}
        </h2>
        {error && <p className="text-red-500 text-center">{error}</p>}
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {!isLogin && (
            <input
              type="text"
              placeholder="Full Name"
              required
              // Added text-gray-900 and placeholder-gray-600
              className="w-full p-2 border rounded text-gray-900 placeholder-gray-600"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
            />
          )}
          <input
            type="email"
            placeholder="Email address"
            required
            // Added text-gray-900 and placeholder-gray-600
            className="w-full p-2 border rounded text-gray-900 placeholder-gray-600"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            type="password"
            placeholder="Password"
            required
            // Added text-gray-900 and placeholder-gray-600
            className="w-full p-2 border rounded text-gray-900 placeholder-gray-600"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button
            type="submit"
            className="w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
          >
            {isLogin ? 'Sign in' : 'Sign up'}
          </button>
        </form>
        <div className="text-center">
          <button onClick={() => setIsLogin(!isLogin)} className="text-indigo-600 hover:text-indigo-500">
            {isLogin ? "Need an account? Sign up" : "Already have an account? Sign in"}
          </button>
        </div>
      </div>
    </div>
  );
}
