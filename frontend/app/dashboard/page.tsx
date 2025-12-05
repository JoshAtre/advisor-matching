'use client';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '../../utils/api';

interface Match {
    advisor: {
        id: number;
        name: string;
        department: string;
        research_areas: string;
    };
    score: number;
    explanation: string;
}

export default function Dashboard() {
  const router = useRouter();
  const [matches, setMatches] = useState<Match[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchMatches();
  }, []);

  const fetchMatches = async () => {
    try {
        const res = await api.get('/matches');
        if (res.status === 400) {
            router.push('/profile'); // Redirect if profile incomplete
            return;
        }
        if (!res.ok) throw new Error('Failed to fetch matches');
        const data = await res.json();
        setMatches(data);
    } catch (err) {
        setError('Could not load matches.');
    } finally {
        setLoading(false);
    }
  };

  const saveAdvisor = async (id: number) => {
      await api.post(`/advisors/${id}/save`, {});
      alert("Advisor saved!");
  };

  if (loading) return <div className="p-8">Finding your best mentors...</div>;

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Your Advisor Matches</h1>
        <div className="space-x-4">
             <button onClick={() => router.push('/profile')} className="text-indigo-600 underline">Edit Profile</button>
             <button onClick={() => {
                 localStorage.removeItem('token');
                 router.push('/');
             }} className="text-red-500">Logout</button>
        </div>
      </div>

      {error && <div className="text-red-500">{error}</div>}
      
      {matches.length === 0 && !error && (
          <div className="text-gray-500">No matches found yet. Try adding more keywords to your profile.</div>
      )}

      <div className="grid gap-6">
        {matches.map((m) => (
            <div key={m.advisor.id} className="border p-6 rounded-lg shadow-sm hover:shadow-md transition bg-white">
                <div className="flex justify-between items-start">
                    <div>
                        <h2 className="text-xl font-bold text-gray-900">{m.advisor.name}</h2>
                        <p className="text-gray-600">{m.advisor.department}</p>
                    </div>
                    <div className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-bold">
                        {m.score}% Match
                    </div>
                </div>
                
                <div className="mt-4">
                    <p className="font-semibold text-sm text-gray-500">WHY THIS MATCH?</p>
                    <p className="text-gray-800 italic mb-2">{m.explanation}</p>
                    
                    <p className="font-semibold text-sm text-gray-500 mt-2">RESEARCH AREAS</p>
                    <p className="text-gray-800">{m.advisor.research_areas}</p>
                </div>

                <div className="mt-4 pt-4 border-t flex justify-end">
                    <button 
                        onClick={() => saveAdvisor(m.advisor.id)}
                        className="text-indigo-600 hover:text-indigo-800 font-medium"
                    >
                        Save to Favorites
                    </button>
                </div>
            </div>
        ))}
      </div>
    </div>
  );
}
