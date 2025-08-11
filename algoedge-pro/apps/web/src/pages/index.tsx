import dynamic from 'next/dynamic';
import Head from 'next/head';

const StrategyBuilder = dynamic(() => import('../ui/StrategyBuilder'), { ssr: false });

export default function Home() {
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
            <StrategyBuilder />
          </div>
          <div className="lg:col-span-2 space-y-4">
            <div className="rounded-lg border border-neutral-800 p-4">
              <h2 className="font-medium mb-2">Backtest</h2>
              <button className="px-3 py-2 rounded bg-indigo-600 hover:bg-indigo-500">Run Backtest</button>
            </div>
            <div className="rounded-lg border border-neutral-800 p-4">
              <h2 className="font-medium mb-2">Optimizer</h2>
              <button className="px-3 py-2 rounded bg-emerald-600 hover:bg-emerald-500">Optimize</button>
            </div>
          </div>
        </div>
      </main>
    </>
  );
}