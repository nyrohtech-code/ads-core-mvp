import React from 'react';
import CampaignCard from './CampaignCard';
import MetricsCard from './MetricsCard';

export default function Dashboard({ client, campaigns }) {
  const totalSpend = campaigns.reduce((sum, c) => sum + (c.spend || 0), 0);
  const totalLeads = campaigns.reduce((sum, c) => sum + (c.conversions || 0), 0);
  const avgRoas = (campaigns.reduce((sum, c) => sum + (c.roas || 0), 0) / campaigns.length).toFixed(2);

  return (
    <div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <MetricsCard title="Spend Total" value={`R$ ${totalSpend.toLocaleString('pt-BR')}`} />
        <MetricsCard title="Leads" value={totalLeads} />
        <MetricsCard title="ROAS Médio" value={`${avgRoas}x`} />
      </div>

      <div className="mb-8">
        <h2 className="text-2xl font-bold mb-4">Campanhas Ativas</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {campaigns.map((campaign) => (
            <CampaignCard key={campaign.id} campaign={campaign} />
          ))}
        </div>
      </div>
    </div>
  );
}
