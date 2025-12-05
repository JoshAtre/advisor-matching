'use client';
import { useState, useEffect } from 'react';
import { api } from '../../utils/api';
import Navbar from '../../components/Navbar';

interface Request {
    id: number;
    status: string;
    message: string;
    created_at: string;
    advisor: {
        name: string;
        department: string;
        image_url: string;
    };
}

export default function Requests() {
  const [requests, setRequests] = useState<Request[]>([]);

  useEffect(() => {
    api.get('/requests').then(async (res) => {
        if(res.ok) setRequests(await res.json());
    });
  }, []);

  const getStatusColor = (status: string) => {
      switch(status) {
          case 'Accepted': return 'bg-green-100 text-green-800';
          case 'Declined': return 'bg-red-100 text-red-800';
          default: return 'bg-yellow-100 text-yellow-800';
      }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-4xl mx-auto p-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">My Meeting Requests</h1>
        
        {requests.length === 0 ? (
            <div className="text-center py-12 bg-white rounded-lg shadow-sm">
                <p className="text-gray-500">You haven't reached out to any advisors yet.</p>
            </div>
        ) : (
            <div className="space-y-4">
                {requests.map((req) => (
                    <div key={req.id} className="bg-white p-6 rounded-lg shadow-sm border border-gray-100 flex items-center justify-between">
                        <div className="flex items-center space-x-4">
                            <img src={req.advisor.image_url} alt="" className="w-12 h-12 rounded-full" />
                            <div>
                                <h3 className="font-bold text-gray-900">{req.advisor.name}</h3>
                                <p className="text-sm text-gray-500">Sent: {new Date(req.created_at).toLocaleDateString()}</p>
                                <p className="text-sm text-gray-600 mt-1">"{req.message}"</p>
                            </div>
                        </div>
                        <div className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(req.status)}`}>
                            {req.status}
                        </div>
                    </div>
                ))}
            </div>
        )}
      </div>
    </div>
  );
}

