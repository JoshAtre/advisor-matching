'use client';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '../../utils/api';

export default function Profile() {
  const router = useRouter();
  const [formData, setFormData] = useState({ interests: '', goals: '', preferred_style: '' });
  
  useEffect(() => {
    // Check auth
    if(!localStorage.getItem('token')) router.push('/');
    
    // Load existing
    api.get('/me').then(async (res) => {
        if(res.ok) {
            const data = await res.json();
            setFormData({
                interests: data.interests || '',
                goals: data.goals || '',
                preferred_style: data.preferred_style || ''
            });
        }
    });
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await api.put('/me/profile', formData);
    if (res.ok) {
      router.push('/dashboard');
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-8">
      <h1 className="text-2xl font-bold mb-6">Complete Your Profile</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
            <label className="block text-sm font-medium text-gray-700">Research Interests</label>
            <textarea
                className="w-full p-2 border rounded h-32"
                placeholder="e.g. Machine Learning, NLP, Robotics"
                value={formData.interests}
                onChange={(e) => setFormData({...formData, interests: e.target.value})}
                required
            />
        </div>
        <div>
            <label className="block text-sm font-medium text-gray-700">Career Goals</label>
            <textarea
                className="w-full p-2 border rounded h-24"
                placeholder="e.g. Become a professor, work in Big Tech R&D"
                value={formData.goals}
                onChange={(e) => setFormData({...formData, goals: e.target.value})}
                required
            />
        </div>
        <div>
            <label className="block text-sm font-medium text-gray-700">Preferred Mentoring Style</label>
            <select
                className="w-full p-2 border rounded"
                value={formData.preferred_style}
                onChange={(e) => setFormData({...formData, preferred_style: e.target.value})}
            >
                <option value="">Select...</option>
                <option value="Hands-on">Hands-on</option>
                <option value="Hands-off">Hands-off</option>
                <option value="Collaborative">Collaborative</option>
            </select>
        </div>
        <button type="submit" className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700">
            Save & Find Matches
        </button>
      </form>
    </div>
  );
}
