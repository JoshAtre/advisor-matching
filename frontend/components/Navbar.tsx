'use client';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

export default function Navbar() {
  const router = useRouter();

  const handleLogout = () => {
    localStorage.removeItem('token');
    router.push('/');
  };

  return (
    <nav className="bg-indigo-600 text-white shadow-lg">
      <div className="max-w-6xl mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-8">
            <Link href="/dashboard" className="font-bold text-xl tracking-tight">
              AdvisorMatch
            </Link>
            <div className="hidden md:flex space-x-4">
              <Link href="/dashboard" className="hover:text-indigo-200 transition">Find Matches</Link>
              <Link href="/requests" className="hover:text-indigo-200 transition">My Requests</Link>
              <Link href="/profile" className="hover:text-indigo-200 transition">Profile</Link>
            </div>
          </div>
          <button 
            onClick={handleLogout}
            className="bg-indigo-700 hover:bg-indigo-800 px-4 py-2 rounded text-sm font-medium transition"
          >
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
}
