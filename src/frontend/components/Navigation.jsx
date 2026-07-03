import React from 'react';
import Link from 'next/link';

export default function Navigation({ clientName }) {
  return (
    <nav className="bg-gray-800 border-b border-gray-700">
      <div className="container mx-auto px-6 py-4">
        <div className="flex justify-between items-center">
          <div>
            <Link href="/">
              <span className="text-2xl font-bold text-blue-400">🚀 ADS CORE</span>
            </Link>
            {clientName && <p className="text-gray-400 text-sm mt-1">{clientName}</p>}
          </div>

          <div className="flex gap-6">
            <Link href="/" className="text-white hover:text-blue-400">
              Dashboard
            </Link>
            <Link href="/campaigns" className="text-white hover:text-blue-400">
              Campanhas
            </Link>
            <Link href="/creatives" className="text-white hover:text-blue-400">
              Criativos
            </Link>
            <Link href="/timeline" className="text-white hover:text-blue-400">
              Timeline
            </Link>
            <Link href="/settings" className="text-white hover:text-blue-400">
              Configurações
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}
