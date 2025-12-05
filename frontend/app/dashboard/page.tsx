'use client';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '../../utils/api';
import Navbar from '../../components/Navbar';

interface Match {
    advisor: {
        id: number;
        name: string;
        department: string;
        research_areas: string;
        image_url: string;
    };
    score: number;
    explanation: string;
}

export default function Dashboard() {
  const router = useRouter();
  const [matches, setMatches] = useState<Match[]>([]);
  const [loading, setLoading] = useState(true);
  const [requestingId, setRequestingId] = useState<number | null>(null);

  useEffect(() => {
    fetchMatches();
  }, []);

  const fetchMatches = async () => {
    try {
        const res = await api.get('/matches');
        if (res.status === 400) {
            router.push('/profile'); 
            return;
        }
        if (!res.ok) throw new Error('Failed');
        setMatches(await res.json());
    } catch (err) {
        console.error(err);
    } finally {
        setLoading(false);
    }
  };

  const handleRequest = async (advisorId: number) => {
    setRequestingId(advisorId);
    const message = prompt("Optional: Include a short message for the advisor?");
    if (message === null) {
        setRequestingId(null);
        return; // User cancelled
    }

    try {
        const res = await api.post('/requests', { advisor_id: advisorId, message: message || "Hi, I'd like to connect!" });
        if (res.ok) {
            alert("Request Sent!");
            router.push('/requests');
        } else {
            const err = await res.json();
            alert(err.detail);
        }
    } finally {
        setRequestingId(null);
    }
  };

  if (loading) return <div className="min-h-screen flex items-center justify-center">Loading matches...</div>;

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-6xl mx-auto p-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Recommended Advisors</h1>
        <p className="text-gray-600 mb-8">Ranked based on your research interests and goals.</p>
        
        <div className="grid md:grid-cols-2 gap-6">
          {matches.map((m) => (
              <div key={m.advisor.id} className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition">
                  <div className="p-6">
                      <div className="flex items-start justify-between">
                          <div className="flex items-center space-x-4">
                              <img src={m.advisor.image_url} alt={m.advisor.name} className="w-16 h-16 rounded-full bg-gray-100" />
                              <div>
                                  <h2 className="text-xl font-bold text-gray-900">{m.advisor.name}</h2>
                                  <p className="text-indigo-600 font-medium">{m.advisor.department}</p>
                              </div>
                          </div>
                          <div className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-bold">
                              {m.score}% Match
                          </div>
                      </div>
                      
                      <div className="mt-4 space-y-3">
                          <div className="bg-gray-50 p-3 rounded-lg">
                            <p className="text-sm font-semibold text-gray-500 uppercase text-xs tracking-wider">Why we matched you</p>
                            <p className="text-gray-800 text-sm mt-1">{m.explanation}</p>
                          </div>
                          <div>
                            <p className="text-sm font-semibold text-gray-500 uppercase text-xs tracking-wider">Research Areas</p>
                            <p className="text-gray-700 text-sm mt-1">{m.advisor.research_areas}</p>
                          </div>
                      </div>

                      <div className="mt-6 flex space-x-3">
                          <button 
                              onClick={() => handleRequest(m.advisor.id)}
                              disabled={requestingId === m.advisor.id}
                              className="flex-1 bg-indigo-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-indigo-700 transition disabled:opacity-50"
                          >
                              {requestingId === m.advisor.id ? 'Sending...' : 'Request Meeting'}
                          </button>
                          <button className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 font-medium">
                              View Profile
                          </button>
                      </div>
                  </div>
              </div>
          ))}
        </div>
      </div>
    </div>
  );
}
