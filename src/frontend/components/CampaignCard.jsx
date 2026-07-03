import React from 'react';

export default function CampaignCard({ campaign }) {
  const statusColor = campaign.status === 'ACTIVE' ? 'bg-green-500' : 'bg-red-500';

  return (
    <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-xl font-bold text-white">{campaign.name}</h3>
          <p className="text-gray-400 text-sm">{campaign.platform}</p>
        </div>
        <span className={`${statusColor} text-white px-3 py-1 rounded-full text-sm`}>
          {campaign.status}
        </span>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div>
          <p className="text-gray-400 text-sm">ROAS</p>
          <p className="text-2xl font-bold text-white">{campaign.roas?.toFixed(2)}x</p>
        </div>
        <div>
          <p className="text-gray-400 text-sm">CPA</p>
          <p className="text-2xl font-bold text-white">R$ {campaign.cpa?.toFixed(2)}</p>
        </div>
        <div>
          <p className="text-gray-400 text-sm">Budget Daily</p>
          <p className="text-2xl font-bold text-white">R$ {campaign.budget_daily?.toLocaleString()}</p>
        </div>
      </div>

      <button className="w-full mt-4 bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
        Ver Detalhes
      </button>
    </div>
  );
}
