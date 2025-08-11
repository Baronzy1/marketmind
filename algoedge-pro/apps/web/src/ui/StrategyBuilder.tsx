import React, { useCallback, useMemo, useState } from 'react';
import ReactFlow, { addEdge, Background, Controls, MiniMap, Node, Edge, Connection } from 'reactflow';
import 'reactflow/dist/style.css';

const initialNodes: Node[] = [
  { id: 'ema_fast', position: { x: 50, y: 50 }, data: { label: 'EMA Fast (20)' }, type: 'input' },
  { id: 'ema_slow', position: { x: 50, y: 150 }, data: { label: 'EMA Slow (50)' }, type: 'input' },
  { id: 'rsi', position: { x: 50, y: 250 }, data: { label: 'RSI (14)' }, type: 'input' },
  { id: 'entry', position: { x: 350, y: 100 }, data: { label: 'Entry' } },
  { id: 'exit', position: { x: 550, y: 100 }, data: { label: 'Exit' } },
  { id: 'risk', position: { x: 350, y: 250 }, data: { label: 'Risk: SL 2% / TP 4%' } },
];

const initialEdges: Edge[] = [
  { id: 'e1', source: 'ema_fast', target: 'entry' },
  { id: 'e2', source: 'ema_slow', target: 'entry' },
  { id: 'e3', source: 'rsi', target: 'entry' },
  { id: 'e4', source: 'entry', target: 'exit' },
];

export default function StrategyBuilder() {
  const [nodes, setNodes] = useState<Node[]>(initialNodes);
  const [edges, setEdges] = useState<Edge[]>(initialEdges);

  const onConnect = useCallback((connection: Connection) => setEdges((eds) => addEdge(connection, eds)), []);

  const dsl = useMemo(() => ({
    version: '0.1',
    name: 'EMA Cross + RSI Filter',
    blocks: [
      { id: 'ema_fast', type: 'indicator', indicator: 'EMA', params: { length: 20, source: 'close' } },
      { id: 'ema_slow', type: 'indicator', indicator: 'EMA', params: { length: 50, source: 'close' } },
      { id: 'rsi', type: 'indicator', indicator: 'RSI', params: { length: 14 } },
      { id: 'entry', type: 'entry', logic: [
        { op: 'cross_over', a: 'ema_fast', b: 'ema_slow' },
        { op: 'lt', a: 'rsi', b: 70 },
      ]},
      { id: 'exit', type: 'exit', logic: [
        { op: 'cross_under', a: 'ema_fast', b: 'ema_slow' },
      ]},
      { id: 'risk', type: 'risk', params: { stop_loss_pct: 0.02, take_profit_pct: 0.04, risk_per_trade_pct: 1.0 } },
    ],
  }), [nodes, edges]);

  return (
    <div className="rounded-lg border border-neutral-800 p-2">
      <div className="h-[520px]">
        <ReactFlow nodes={nodes} edges={edges} onNodesChange={setNodes as any} onEdgesChange={setEdges as any} onConnect={onConnect} fitView>
          <MiniMap />
          <Controls />
          <Background />
        </ReactFlow>
      </div>
      <div className="mt-3">
        <h3 className="text-sm font-medium mb-1">Strategy JSON</h3>
        <pre className="text-xs bg-neutral-900 p-3 rounded overflow-auto max-h-64">{JSON.stringify(dsl, null, 2)}</pre>
      </div>
    </div>
  );
}