import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Dashboard from '../components/Dashboard';
import Navigation from '../components/Navigation';

export default function Home() {
  const [client, setClient] = useState(null);
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      // TODO: Conectar ao Supabase
      // const response = await axios.get('/api/dashboard/data');
      // setClient(response.data.client);
      // setCampaigns(response.data.campaigns);

      // Por enquanto, usar dados dummy
      setClient({
        name: 'Cliente Demo',
        budget_monthly: 5000,
        timezone: 'America/Sao_Paulo',
      });
      setCampaigns([
        {
          id: 'campaign_001',
          name: 'E-commerce - Black Friday',
          status: 'ACTIVE',
          roas: 2.98,
          cpa: 228,
          budget_daily: 1000,
        },
        {
          id: 'campaign_002',
          name: 'SaaS - Lead Gen',
          status: 'ACTIVE',
          roas: 1.88,
          cpa: 266.67,
          budget_daily: 500,
        },
      ]);
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="flex items-center justify-center h-screen">Carregando...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Navigation clientName={client?.name} />
      <main className="container mx-auto p-6">
        <Dashboard client={client} campaigns={campaigns} />
      </main>
    </div>
  );
}
