import dynamic from 'next/dynamic';
import Head from 'next/head';
import { useRef, useState } from 'react';
import type { StrategyBuilderHandle } from '../ui/StrategyBuilder';

const StrategyBuilder = dynamic(() => import('../ui/StrategyBuilder'), { ssr: false });

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function Home() {
  const builderRef = useRef<StrategyBuilderHandle>(null);
  const [backtestResult, setBacktestResult] = useState<any>(null);
  const [optimizeResult, setOptimizeResult] = useState<any>(null);
  const [loading, setLoading] = useState<string | null>(null);

  async function handleBacktest() {
    try {
      setLoading('backtest');
      const dsl = builderRef.current?.getDSL();
      const res = await fetch(`${API_URL}/strategies/backtest`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ strategy: dsl, symbol: 'BTC/USDT', market: 'crypto', timeframe: '1h', years: 2 }),
      });
      const data = await res.json();
      setBacktestResult(data);
    } finally {
      setLoading(null);
    }
  }

  async function handleOptimize() {
    try {
      setLoading('optimize');
      const dsl = builderRef.current?.getDSL();
      const param_space = {
        ema_fast: { length: { type: 'int', min: 5, max: 50 } },
        ema_slow: { length: { type: 'int', min: 20, max: 200 } },
      };
      const res = await fetch(`${API_URL}/strategies/optimize`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ strategy: dsl, param_space, objective: 'roi_pct', symbol: 'BTC/USDT', market: 'crypto', timeframe: '1h', years: 2, samples: 15 }),
      });
      const data = await res.json();
      setOptimizeResult(data);
    } finally {
      setLoading(null);
    }
  }

  return (
    <>
      <Head>
        <title>AlgoEdge Pro</title>
      </Head>
      <main className="p-4">
        <h1 className="text-2xl font-semibold mb-4">AlgoEdge Pro</h1>
        <p className="text-sm text-neutral-400 mb-6">Design, test, and deploy automated strategies without code.</p>
        <div className="grid grid-cols-1 lg:grid-cols-5 gap-4">
          <div className="lg:col-span-3">
            <StrategyBuilder ref={builderRef} />
          </div>
          <div className="lg:col-span-2 space-y-4">
            <div className="rounded-lg border border-neutral-800 p-4 space-y-2">
              <h2 className="font-medium">Backtest</h2>
              <button onClick={handleBacktest} disabled={loading==='backtest'} className="px-3 py-2 rounded bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50">{loading==='backtest' ? 'Running...' : 'Run Backtest'}</button>
              {backtestResult && (
                <pre className="text-xs bg-neutral-900 p-3 rounded overflow-auto max-h-64">{JSON.stringify(backtestResult, null, 2)}</pre>
              )}
            </div>
            <div className="rounded-lg border border-neutral-800 p-4 space-y-2">
              <h2 className="font-medium">Optimizer</h2>
              <button onClick={handleOptimize} disabled={loading==='optimize'} className="px-3 py-2 rounded bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50">{loading==='optimize' ? 'Optimizing...' : 'Optimize'}</button>
              {optimizeResult && (
                <pre className="text-xs bg-neutral-900 p-3 rounded overflow-auto max-h-64">{JSON.stringify(optimizeResult, null, 2)}</pre>
              )}
            </div>
          </div>
        </div>
      </main>
    </>
  );
}