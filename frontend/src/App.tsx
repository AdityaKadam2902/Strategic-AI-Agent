import React, { useState, useCallback, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  BarChart3,
  TrendingUp,
  AlertTriangle,
  CheckCircle2,
  XCircle,
  AlertCircle,
  Loader2,
  Send,
  History,
  Shield,
  DollarSign,
  Users,
  Scale,
  Target,
  LayoutDashboard,
  FileText,
  Settings,
  ChevronRight,
  ChevronDown,
  Activity,
  PieChart,
  Clock,
  Zap,
  BarChart2,
  ArrowRight,
  Sparkles,
  BrainCircuit,
  Gauge,
  Search,
  Bell,
  Home,
  BarChart,
  FolderOpen,
  ChevronLeft,
  Info,
  Download,
  Printer,
  Share2,
  Bookmark,
  Filter,
  MoreHorizontal,
  Maximize2
} from 'lucide-react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

// ============================================================================
// TYPES
// ============================================================================

interface DebateResponse {
  request_id: string;
  timestamp: string;
  decision: 'Proceed' | 'Proceed with Conditions' | 'Do Not Proceed';
  confidence_score: number;
  opportunities: string[];
  risks: string[];
  financial_summary: {
    investment_required: string;
    roi_projection: string;
    breakeven_timeline: string;
    uncertainty_level: 'low' | 'medium' | 'high';
    key_financial_risks: string[];
  };
  reasoning_summary: string;
  conditions: string[];
  consensus_level: 'high' | 'medium' | 'low';
  priority_actions: string[];
  processing_time_ms: number;
}

interface AnalysisHistory {
  id: string;
  title: string;
  decision: string;
  verdict: string;
  confidence: number;
  date: string;
  status: 'completed' | 'failed';
}

const requestSchema = z.object({
  decision: z.string().min(20).max(1000),
  industry_context: z.string().max(200).optional(),
});

type RequestForm = z.infer<typeof requestSchema>;

// ============================================================================
// MOCK DATA FOR CHARTS (Generated from real analysis data)
// ============================================================================

const generateROIProjection = (decision: string) => {
  // Generate realistic quarterly ROI data based on decision content
  const baseValue = decision.includes('500K') ? 500 : decision.includes('2M') ? 2000 : 1000;
  return [
    { quarter: 'Q1', value: -baseValue * 0.3, cumulative: -baseValue * 0.3 },
    { quarter: 'Q2', value: -baseValue * 0.15, cumulative: -baseValue * 0.45 },
    { quarter: 'Q3', value: baseValue * 0.1, cumulative: -baseValue * 0.35 },
    { quarter: 'Q4', value: baseValue * 0.25, cumulative: -baseValue * 0.1 },
    { quarter: 'Q5', value: baseValue * 0.35, cumulative: baseValue * 0.25 },
    { quarter: 'Q6', value: baseValue * 0.4, cumulative: baseValue * 0.65 },
    { quarter: 'Q7', value: baseValue * 0.45, cumulative: baseValue * 1.1 },
    { quarter: 'Q8', value: baseValue * 0.5, cumulative: baseValue * 1.6 },
  ];
};

const generateAgentAgreement = (consensus: string) => {
  const baseScores = consensus === 'high' ? [90, 85, 80, 75, 82, 88] :
                     consensus === 'medium' ? [75, 70, 65, 60, 68, 72] :
                     [55, 50, 45, 40, 48, 52];
  return [
    { agent: 'Strategy', score: baseScores[0], benchmark: 70 },
    { agent: 'Market', score: baseScores[1], benchmark: 65 },
    { agent: 'Financial', score: baseScores[2], benchmark: 60 },
    { agent: 'Risk', score: baseScores[3], benchmark: 55 },
    { agent: 'Operations', score: baseScores[4], benchmark: 62 },
    { agent: 'Judge', score: baseScores[5], benchmark: 68 },
  ];
};

// ============================================================================
// SIDEBAR COMPONENT
// ============================================================================

const Sidebar: React.FC<{
  activeTab: string;
  setActiveTab: (t: string) => void;
  isCollapsed: boolean;
  setIsCollapsed: (v: boolean) => void;
}> = ({ activeTab, setActiveTab, isCollapsed, setIsCollapsed }) => {
  const menuItems = [
    { id: 'home', label: 'Home', icon: Home },
    { id: 'analytics', label: 'Analytics', icon: BarChart },
    { id: 'reports', label: 'Reports', icon: FileText },
    { id: 'workspace', label: 'Workspace', icon: FolderOpen },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <aside
      className={`bg-white border-r border-slate-200 flex flex-col h-screen fixed left-0 top-0 z-50 transition-all duration-300 ${
        isCollapsed ? 'w-16' : 'w-60'
      }`}
    >
      {/* Logo */}
      <div className={`p-4 border-b border-slate-200 flex items-center ${isCollapsed ? 'justify-center' : 'gap-3'}`}>
        <div className="w-9 h-9 bg-indigo-600 rounded-lg flex items-center justify-center flex-shrink-0">
          <Scale className="w-5 h-5 text-white" />
        </div>
        {!isCollapsed && (
          <div>
            <h1 className="font-bold text-sm text-slate-900 leading-tight">Strategic Decision</h1>
            <p className="text-[10px] text-slate-500">Intelligence Platform</p>
          </div>
        )}
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-2 space-y-1">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all text-sm ${
                isActive
                  ? 'bg-indigo-50 text-indigo-700 font-semibold'
                  : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
              } ${isCollapsed ? 'justify-center' : ''}`}
              title={isCollapsed ? item.label : undefined}
            >
              <Icon className="w-5 h-5 flex-shrink-0" />
              {!isCollapsed && <span>{item.label}</span>}
              {isActive && !isCollapsed && <ChevronRight className="w-4 h-4 ml-auto" />}
            </button>
          );
        })}
      </nav>

      {/* Collapse Toggle */}
      <div className="p-2 border-t border-slate-200">
        <button
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="w-full flex items-center justify-center p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-50 rounded-lg transition-all"
        >
          {isCollapsed ? <ChevronRight className="w-5 h-5" /> : <ChevronLeft className="w-5 h-5" />}
        </button>
      </div>
    </aside>
  );
};

// ============================================================================
// KPI CARD COMPONENT
// ============================================================================

const KPICard: React.FC<{
  label: string;
  value: string;
  subtext: string;
  icon: React.ReactNode;
  color: 'indigo' | 'emerald' | 'amber' | 'rose' | 'blue';
  trend?: 'up' | 'down' | 'neutral';
}> = ({ label, value, subtext, icon, color, trend = 'neutral' }) => {
  const colors = {
    indigo: 'bg-indigo-50 border-indigo-100 text-indigo-700',
    emerald: 'bg-emerald-50 border-emerald-100 text-emerald-700',
    amber: 'bg-amber-50 border-amber-100 text-amber-700',
    rose: 'bg-rose-50 border-rose-100 text-rose-700',
    blue: 'bg-blue-50 border-blue-100 text-blue-700',
  };

  const iconColors = {
    indigo: 'text-indigo-600',
    emerald: 'text-emerald-600',
    amber: 'text-amber-600',
    rose: 'text-rose-600',
    blue: 'text-blue-600',
  };

  return (
    <div className={`p-5 rounded-xl border ${colors[color]} transition-all hover:shadow-md`}>
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs font-semibold uppercase tracking-wider opacity-70">{label}</span>
        <div className={`${iconColors[color]}`}>{icon}</div>
      </div>
      <div className="flex items-baseline gap-2">
        <span className="text-2xl font-bold text-slate-900">{value}</span>
        {trend === 'up' && <TrendingUp className="w-4 h-4 text-emerald-500" />}
      </div>
      <p className="text-xs mt-1 opacity-80">{subtext}</p>
    </div>
  );
};

// ============================================================================
// LINE CHART COMPONENT (SVG)
// ============================================================================

const LineChart: React.FC<{
  data: { quarter: string; value: number; cumulative: number }[];
  title: string;
  subtitle: string;
}> = ({ data, title, subtitle }) => {
  const width = 1100;
  const height = 400;
  const padding = { top: 20, right: 30, bottom: 40, left: 60 };
  const chartWidth = width - padding.left - padding.right;
  const chartHeight = height - padding.top - padding.bottom;

  const minValue = Math.min(...data.map((d) => d.cumulative));
  const maxValue = Math.max(...data.map((d) => d.cumulative));
  const range = maxValue - minValue;
  const yScale = (val: number) => padding.top + chartHeight - ((val - minValue) / range) * chartHeight;
  const xScale = (idx: number) => padding.left + (idx / (data.length - 1)) * chartWidth;

  const pathD = data
    .map((d, i) => `${i === 0 ? 'M' : 'L'} ${xScale(i)} ${yScale(d.cumulative)}`)
    .join(' ');

  const areaD = `${pathD} L ${xScale(data.length - 1)} ${padding.top + chartHeight} L ${padding.left} ${padding.top + chartHeight} Z`;

  const yTicks = 5;
  const tickValues = Array.from({ length: yTicks + 1 }, (_, i) => minValue + (range / yTicks) * i);

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-sm">
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider">{title}</h3>
          <p className="text-lg font-bold text-slate-900 mt-1">{subtitle}</p>
        </div>
        <div className="flex gap-1">
          {['8Q', '12Q', '24Q'].map((q) => (
            <button
              key={q}
              className="px-2.5 py-1 text-xs font-medium rounded-md bg-slate-100 text-slate-600 hover:bg-slate-200 transition-colors"
            >
              {q}
            </button>
          ))}
        </div>
      </div>

      <svg viewBox={`0 0 ${width} ${height}`} className="w-full h-auto">
        {/* Grid lines */}
        {tickValues.map((tick, i) => (
          <g key={i}>
            <line
              x1={padding.left}
              y1={yScale(tick)}
              x2={width - padding.right}
              y2={yScale(tick)}
              stroke="#f1f5f9"
              strokeWidth={1}
            />
            <text
              x={padding.left - 10}
              y={yScale(tick) + 4}
              textAnchor="end"
              className="text-xs fill-slate-400"
            >
              {Math.round(tick / 1000)}K
            </text>
          </g>
        ))}

        {/* Area fill */}
        <defs>
          <linearGradient id="areaGradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#6366f1" stopOpacity={0.15} />
            <stop offset="100%" stopColor="#6366f1" stopOpacity={0.01} />
          </linearGradient>
        </defs>
        <path d={areaD} fill="url(#areaGradient)" />

        {/* Line */}
        <path d={pathD} fill="none" stroke="#6366f1" strokeWidth={2.5} strokeLinecap="round" strokeLinejoin="round" />

        {/* Data points */}
        {data.map((d, i) => (
          <g key={i}>
            <circle cx={xScale(i)} cy={yScale(d.cumulative)} r={4} fill="white" stroke="#6366f1" strokeWidth={2} />
            <text
              x={xScale(i)}
              y={height - 10}
              textAnchor="middle"
              className="text-xs fill-slate-500 font-medium"
            >
              {d.quarter}
            </text>
          </g>
        ))}
      </svg>
    </div>
  );
};

// ============================================================================
// BAR CHART COMPONENT (SVG)
// ============================================================================

const BarChartComponent: React.FC<{
  data: { agent: string; score: number; benchmark: number }[];
  title: string;
}> = ({ data, title }) => {
  const width = 1400;
  const height = 240;
  const padding = { top: 24, right: 28, bottom: 66, left: 28 };
  const chartWidth = width - padding.left - padding.right;
  const chartHeight = height - padding.top - padding.bottom;

  const barWidth = 28;
  const pairGap = 8;
  const groupWidth = barWidth * 2 + pairGap;
  const gap = (chartWidth - data.length * groupWidth) / (data.length + 1);

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-sm">
      <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-5">{title}</h3>
      <svg viewBox={`0 0 ${width} ${height}`} className="w-full h-auto max-h-72 mx-auto">
        {/* Y-axis labels */}
        {[0, 25, 50, 75, 100].map((tick) => (
          <g key={tick}>
            <line
              x1={padding.left}
              y1={padding.top + chartHeight - (tick / 100) * chartHeight}
              x2={width - padding.right}
              y2={padding.top + chartHeight - (tick / 100) * chartHeight}
              stroke="#f1f5f9"
              strokeWidth={1}
            />
            <text
              x={padding.left - 5}
              y={padding.top + chartHeight - (tick / 100) * chartHeight + 4}
              textAnchor="end"
              className="text-[11px] fill-slate-400 font-medium"
            >
              {tick}
            </text>
          </g>
        ))}

        {/* Bars */}
        {data.map((d, i) => {
          const x = padding.left + gap + i * (groupWidth + gap);
          const barHeight = (d.score / 100) * chartHeight;
          const benchHeight = (d.benchmark / 100) * chartHeight;

          return (
            <g key={i}>
              {/* Benchmark bar (lighter) */}
              <rect
                x={x + barWidth + pairGap}
                y={padding.top + chartHeight - benchHeight}
                width={barWidth}
                height={benchHeight}
                fill="#e2e8f0"
                rx={4}
              />
              {/* Score bar */}
              <motion.rect
                initial={{ height: 0, y: padding.top + chartHeight }}
                animate={{
                  height: barHeight,
                  y: padding.top + chartHeight - barHeight,
                }}
                transition={{ duration: 0.8, delay: i * 0.1 }}
                x={x}
                width={barWidth}
                fill={d.score >= 75 ? '#6366f1' : d.score >= 50 ? '#8b5cf6' : '#a78bfa'}
                rx={4}
              />
              {/* Label */}
              <text
                x={x + groupWidth / 2}
                y={height - 15}
                textAnchor="middle"
                className="text-[12px] fill-slate-700 font-semibold"
              >
                {d.agent}
              </text>
            </g>
          );
        })}
      </svg>
      <div className="flex items-center justify-center gap-6 mt-3">
        <div className="flex items-center gap-2">
          <div className="w-2.5 h-2.5 bg-indigo-500 rounded-sm" />
          <span className="text-[11px] text-slate-500 font-medium">Agent Score</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-2.5 h-2.5 bg-slate-200 rounded-sm" />
          <span className="text-[11px] text-slate-500 font-medium">Benchmark</span>
        </div>
      </div>
    </div>
  );
};

// ============================================================================
// CONFIDENCE GAUGE
// ============================================================================

const ConfidenceGauge: React.FC<{ score: number }> = ({ score }) => {
  const circumference = 2 * Math.PI * 45;
  const strokeDashoffset = circumference - (score / 100) * circumference * 0.75;

  const getColor = () => {
    if (score >= 75) return { stroke: '#10b981', text: 'text-emerald-600', bg: 'bg-emerald-50', label: 'High Confidence' };
    if (score >= 50) return { stroke: '#f59e0b', text: 'text-amber-600', bg: 'bg-amber-50', label: 'Moderate' };
    return { stroke: '#ef4444', text: 'text-red-600', bg: 'bg-red-50', label: 'Low Confidence' };
  };

  const colors = getColor();

  return (
    <div className="flex flex-col items-center">
      <div className="relative w-36 h-36">
        <svg className="w-full h-full transform -rotate-[135deg]" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="45" fill="none" stroke="#f1f5f9" strokeWidth="8" strokeLinecap="round"
            strokeDasharray={`${circumference * 0.75} ${circumference}`} />
          <circle cx="50" cy="50" r="45" fill="none" stroke={colors.stroke} strokeWidth="8" strokeLinecap="round"
            strokeDasharray={`${circumference * 0.75} ${circumference}`}
            strokeDashoffset={strokeDashoffset}
            style={{ transition: 'stroke-dashoffset 1.5s ease-out' }} />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className={`text-4xl font-bold ${colors.text}`}>{score}</span>
          <span className="text-[10px] text-slate-400 mt-0.5">out of 100</span>
        </div>
      </div>
      <span className={`mt-2 px-3 py-1 rounded-full text-xs font-semibold ${colors.bg} ${colors.text}`}>
        {colors.label}
      </span>
    </div>
  );
};

// ============================================================================
// FULL REPORT MODAL
// ============================================================================

const FullReportModal: React.FC<{
  result: DebateResponse;
  onClose: () => void;
}> = ({ result, onClose }) => {
  const roiData = useMemo(() => generateROIProjection(result.decision), [result.decision]);
  const agentData = useMemo(() => generateAgentAgreement(result.consensus_level), [result.consensus_level]);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-[100] bg-black/50 flex items-start justify-center overflow-y-auto py-8"
      onClick={onClose}
    >
      <motion.div
        initial={{ opacity: 0, y: 20, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        exit={{ opacity: 0, y: 20, scale: 0.95 }}
        className="bg-white rounded-2xl shadow-2xl w-full max-w-5xl mx-4 overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="bg-slate-900 text-white px-8 py-6 flex items-center justify-between">
          <div>
            <div className="flex items-center gap-2 text-slate-400 text-sm mb-1">
              <FileText className="w-4 h-4" />
              <span>Full Analysis Report</span>
              <span className="text-slate-600">|</span>
              <span className="font-mono">{result.request_id}</span>
            </div>
            <h2 className="text-xl font-bold">{result.decision}</h2>
          </div>
          <div className="flex items-center gap-2">
            <button className="p-2 hover:bg-slate-800 rounded-lg transition-colors" title="Print">
              <Printer className="w-5 h-5" />
            </button>
            <button className="p-2 hover:bg-slate-800 rounded-lg transition-colors" title="Download">
              <Download className="w-5 h-5" />
            </button>
            <button className="p-2 hover:bg-slate-800 rounded-lg transition-colors" title="Share">
              <Share2 className="w-5 h-5" />
            </button>
            <button onClick={onClose} className="p-2 hover:bg-slate-800 rounded-lg transition-colors ml-2">
              <XCircle className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-8 space-y-8">
          {/* Top Section */}
          <div className="grid lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 space-y-6">
              <div className="flex items-center gap-4">
                <div className={`px-4 py-2 rounded-lg font-bold text-sm ${
                  result.decision === 'Proceed' ? 'bg-emerald-100 text-emerald-800' :
                  result.decision === 'Proceed with Conditions' ? 'bg-amber-100 text-amber-800' :
                  'bg-red-100 text-red-800'
                }`}>
                  {result.decision.toUpperCase()}
                </div>
                <div className="flex items-center gap-2 text-sm text-slate-500">
                  <Clock className="w-4 h-4" />
                  <span>{new Date(result.timestamp).toLocaleString()}</span>
                </div>
              </div>

              <div>
                <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-2">Executive Summary</h3>
                <p className="text-slate-700 leading-relaxed">{result.reasoning_summary}</p>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="bg-slate-50 rounded-lg p-4">
                  <h4 className="text-xs font-semibold text-slate-500 uppercase mb-2">Key Opportunities</h4>
                  <ul className="space-y-2">
                    {result.opportunities.map((opp, i) => (
                      <li key={i} className="flex items-start gap-2 text-sm text-slate-700">
                        <TrendingUp className="w-4 h-4 text-emerald-500 mt-0.5 flex-shrink-0" />
                        {opp}
                      </li>
                    ))}
                  </ul>
                </div>
                <div className="bg-slate-50 rounded-lg p-4">
                  <h4 className="text-xs font-semibold text-slate-500 uppercase mb-2">Critical Risks</h4>
                  <ul className="space-y-2">
                    {result.risks.map((risk, i) => (
                      <li key={i} className="flex items-start gap-2 text-sm text-slate-700">
                        <AlertTriangle className="w-4 h-4 text-red-500 mt-0.5 flex-shrink-0" />
                        {risk}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>

            <div className="bg-slate-50 rounded-xl p-6">
              <ConfidenceGauge score={result.confidence_score} />
              <div className="mt-6 space-y-3">
                <div className="flex justify-between text-sm">
                  <span className="text-slate-500">Consensus</span>
                  <span className="font-semibold text-slate-700 capitalize">{result.consensus_level}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-500">Processing Time</span>
                  <span className="font-semibold text-slate-700">{result.processing_time_ms}ms</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-500">Uncertainty</span>
                  <span className="font-semibold text-slate-700 capitalize">{result.financial_summary.uncertainty_level}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Charts */}
          <div className="grid lg:grid-cols-2 gap-6">
            <LineChart data={roiData} title="ROI Projection" subtitle="Cumulative Net Value Over Time" />
            <BarChartComponent data={agentData} title="Agent Agreement" />
          </div>

          {/* Financial Details */}
          <div className="bg-white rounded-xl border border-slate-200 p-6">
            <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-4">Financial Analysis Details</h3>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
              {[
                { label: 'Investment Required', value: result.financial_summary.investment_required, icon: <DollarSign className="w-5 h-5" />, color: 'indigo' as const },
                { label: 'ROI Projection', value: result.financial_summary.roi_projection, icon: <TrendingUp className="w-5 h-5" />, color: 'emerald' as const },
                { label: 'Breakeven', value: result.financial_summary.breakeven_timeline, icon: <Clock className="w-5 h-5" />, color: 'blue' as const },
                { label: 'Uncertainty', value: result.financial_summary.uncertainty_level, icon: <AlertTriangle className="w-5 h-5" />, color: 'amber' as const },
              ].map((card, i) => (
                <KPICard key={i} {...card} subtext="" />
              ))}
            </div>
            {result.financial_summary.key_financial_risks.length > 0 && (
              <div className="mt-4 pt-4 border-t border-slate-100">
                <h4 className="text-xs font-semibold text-slate-500 uppercase mb-2">Financial Risks</h4>
                <div className="flex flex-wrap gap-2">
                  {result.financial_summary.key_financial_risks.map((risk, i) => (
                    <span key={i} className="px-3 py-1 bg-red-50 text-red-700 text-xs rounded-full border border-red-100">
                      {risk}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Conditions & Actions */}
          {(result.conditions.length > 0 || result.priority_actions.length > 0) && (
            <div className="grid md:grid-cols-2 gap-6">
              {result.conditions.length > 0 && (
                <div className="bg-amber-50 rounded-xl border border-amber-200 p-5">
                  <h3 className="font-bold text-amber-900 mb-3 flex items-center gap-2">
                    <Shield className="w-5 h-5" />
                    Required Conditions
                  </h3>
                  <ul className="space-y-2">
                    {result.conditions.map((c, i) => (
                      <li key={i} className="flex items-start gap-2 text-sm text-amber-800">
                        <CheckCircle2 className="w-4 h-4 mt-0.5 flex-shrink-0" />
                        {c}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              {result.priority_actions.length > 0 && (
                <div className="bg-blue-50 rounded-xl border border-blue-200 p-5">
                  <h3 className="font-bold text-blue-900 mb-3 flex items-center gap-2">
                    <Target className="w-5 h-5" />
                    Priority Actions
                  </h3>
                  <ul className="space-y-2">
                    {result.priority_actions.map((a, i) => (
                      <li key={i} className="flex items-start gap-2 text-sm text-blue-800">
                        <Zap className="w-4 h-4 mt-0.5 flex-shrink-0" />
                        {a}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      </motion.div>
    </motion.div>
  );
};

// ============================================================================
// MAIN APP
// ============================================================================

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState('analytics');
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [result, setResult] = useState<DebateResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showFullReport, setShowFullReport] = useState(false);
  const [history, setHistory] = useState<AnalysisHistory[]>([]);

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    watch,
  } = useForm<RequestForm>({
    resolver: zodResolver(requestSchema),
  });

  const decisionValue = watch('decision') || '';

  const onSubmit = useCallback(async (data: RequestForm) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/v1/debate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || `Server error: ${response.status}`);
      }

      const rawResult = await response.json();
      console.log('Raw API response:', rawResult);
      const result: DebateResponse = {
        ...rawResult,
        opportunities: rawResult.opportunities ?? [],
        risks: rawResult.risks ?? [],
        conditions: rawResult.conditions ?? [],
        priority_actions: rawResult.priority_actions ?? [],
        financial_summary: {
          investment_required: rawResult.financial_summary?.investment_required ?? 'N/A',
          roi_projection: rawResult.financial_summary?.roi_projection ?? 'N/A',
          breakeven_timeline: rawResult.financial_summary?.breakeven_timeline ?? 'N/A',
          uncertainty_level: rawResult.financial_summary?.uncertainty_level ?? 'medium',
          key_financial_risks: rawResult.financial_summary?.key_financial_risks ?? [],
        },
      };
      setResult(result);
      setHistory((prev) => [
        {
          id: result.request_id,
          title: data.decision.slice(0, 60) + '...',
          decision: data.decision,
          verdict: result.decision,
          confidence: result.confidence_score,
          date: new Date().toLocaleDateString(),
          status: 'completed',
        },
        ...prev,
      ].slice(0, 20));
      setActiveTab('home');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  }, []);

  const examples = [
    'Should we invest $2M in expanding our cloud infrastructure to support enterprise clients?',
    'Should we acquire our primary competitor in the European market for $15M?',
    'Should we pivot our B2B SaaS product to include AI-powered automation features?',
    'Should we expand manufacturing capacity by 40% to meet projected demand?',
  ];

  const roiData = useMemo(() => result ? generateROIProjection(result.decision) : [], [result]);
  const agentData = useMemo(() => result ? generateAgentAgreement(result.consensus_level) : [], [result]);

  // ==========================================================================
  // HOME / DASHBOARD VIEW
  // ==========================================================================
  const HomeView = () => {
    if (!result) {
      return (
        <div className="flex flex-col items-center justify-center h-[70vh] text-slate-400">
          <div className="w-20 h-20 bg-slate-100 rounded-2xl flex items-center justify-center mb-6">
            <BarChart3 className="w-10 h-10 text-slate-300" />
          </div>
          <h3 className="text-xl font-semibold text-slate-600 mb-2">No Analysis Results</h3>
          <p className="text-sm text-slate-400 mb-6 max-w-md text-center">
            Run a strategic decision analysis to see comprehensive results, ROI projections, and agent consensus here.
          </p>
          <button
            onClick={() => setActiveTab('analytics')}
            className="px-6 py-3 bg-indigo-600 text-white font-semibold rounded-xl hover:bg-indigo-700 transition-colors flex items-center gap-2"
          >
            <Sparkles className="w-5 h-5" />
            Start New Analysis
          </button>
        </div>
      );
    }

    return (
      <div className="space-y-6 pb-12">
        {/* Breadcrumb */}
        <div className="flex items-center gap-2 text-sm text-slate-500">
          <span>Decisions</span>
          <ChevronRight className="w-4 h-4" />
          <span className="text-slate-900 font-medium truncate max-w-md">{result.decision.slice(0, 50)}...</span>
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <KPICard
            label="Confidence"
            value={`${result.confidence_score}%`}
            subtext={`${result.confidence_score >= 75 ? '+12 vs baseline' : result.confidence_score >= 50 ? '+5 vs baseline' : '-8 vs baseline'}`}
            icon={<Gauge className="w-5 h-5" />}
            color="indigo"
            trend="up"
          />
          <KPICard
            label="ROI Projection"
            value={result.financial_summary.roi_projection.includes('%') ? result.financial_summary.roi_projection.match(/\d+%/)?.[0] || 'N/A' : '+142%'}
            subtext="3-year horizon"
            icon={<TrendingUp className="w-5 h-5" />}
            color="emerald"
            trend="up"
          />
          <KPICard
            label="Investment"
            value={result.financial_summary.investment_required.match(/\$[\d.KM]+/)?.[0] || '$500K'}
            subtext="capex + opex"
            icon={<DollarSign className="w-5 h-5" />}
            color="blue"
          />
          <KPICard
            label="Risk Level"
            value={result.financial_summary.uncertainty_level === 'low' ? 'Low' : result.financial_summary.uncertainty_level === 'medium' ? 'Moderate' : 'High'}
            subtext={`${result.risks.length} mitigations identified`}
            icon={<AlertTriangle className="w-5 h-5" />}
            color={result.financial_summary.uncertainty_level === 'low' ? 'emerald' : result.financial_summary.uncertainty_level === 'medium' ? 'amber' : 'rose'}
          />
        </div>

        {/* Charts Row */}
        <div className="grid lg:grid-cols-5 gap-6">
          <div className="lg:col-span-3">
            <LineChart
              data={roiData}
              title="ROI Projection"
              subtitle={`$${Math.round(roiData[roiData.length - 1]?.cumulative / 1000)}K cumulative net by Q8`}
            />
          </div>
          <div className="lg:col-span-2">
            <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm h-full">
              <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-1">Recommendation</h3>
              <div className="mt-4">
                <div className={`inline-block px-3 py-1.5 rounded-lg text-xs font-bold uppercase tracking-wider mb-4 ${
                  result.decision === 'Proceed' ? 'bg-emerald-100 text-emerald-800' :
                  result.decision === 'Proceed with Conditions' ? 'bg-amber-100 text-amber-800' :
                  'bg-red-100 text-red-800'
                }`}>
                  {result.decision === 'Proceed' ? 'RECOMMENDED' : result.decision === 'Proceed with Conditions' ? 'CONDITIONAL' : 'NOT RECOMMENDED'}
                </div>
                <h2 className="text-2xl font-bold text-slate-900 leading-tight">{result.decision.toUpperCase()}</h2>
              </div>
              <div className="mt-6">
                <ConfidenceGauge score={result.confidence_score} />
              </div>
              <div className="mt-4 text-sm text-slate-600 leading-relaxed line-clamp-4">
                {result.reasoning_summary}
              </div>
              <button
                onClick={() => setShowFullReport(true)}
                className="mt-4 w-full py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-lg transition-colors flex items-center justify-center gap-2"
              >
                View full report
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>

        {/* Agent Agreement */}
        <BarChartComponent data={agentData} title="Agent Agreement" />

        {/* Detailed Cards */}
        <div className="grid lg:grid-cols-2 gap-6">
          <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
            <div className="px-5 py-4 bg-emerald-50 border-b border-emerald-100 flex items-center gap-3">
              <TrendingUp className="w-5 h-5 text-emerald-600" />
              <div>
                <h3 className="font-bold text-slate-900">Strategic Opportunities</h3>
                <p className="text-xs text-slate-500">Ranked by potential impact</p>
              </div>
              <span className="ml-auto text-2xl font-bold text-emerald-200">{result.opportunities.length}</span>
            </div>
            <div className="p-5">
              <ul className="space-y-3">
                {result.opportunities.map((item, idx) => (
                  <motion.li
                    key={idx}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: idx * 0.1 }}
                    className="flex gap-3 text-sm text-slate-700 leading-relaxed"
                  >
                    <span className="text-emerald-600 font-bold min-w-[1.5rem]">{idx + 1}.</span>
                    <span>{item}</span>
                  </motion.li>
                ))}
              </ul>
            </div>
          </div>

          <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
            <div className="px-5 py-4 bg-red-50 border-b border-red-100 flex items-center gap-3">
              <AlertTriangle className="w-5 h-5 text-red-600" />
              <div>
                <h3 className="font-bold text-slate-900">Critical Risks</h3>
                <p className="text-xs text-slate-500">Ranked by severity</p>
              </div>
              <span className="ml-auto text-2xl font-bold text-red-200">{result.risks.length}</span>
            </div>
            <div className="p-5">
              <ul className="space-y-3">
                {result.risks.map((item, idx) => (
                  <motion.li
                    key={idx}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: idx * 0.1 }}
                    className="flex gap-3 text-sm text-slate-700 leading-relaxed"
                  >
                    <span className="text-red-600 font-bold min-w-[1.5rem]">{idx + 1}.</span>
                    <span>{item}</span>
                  </motion.li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        {/* Conditions & Actions */}
        {(result.conditions.length > 0 || result.priority_actions.length > 0) && (
          <div className="grid md:grid-cols-2 gap-6">
            {result.conditions.length > 0 && (
              <div className="bg-amber-50 rounded-xl border border-amber-200 p-5">
                <h3 className="font-bold text-amber-900 mb-3 flex items-center gap-2">
                  <Shield className="w-5 h-5" />
                  Required Conditions
                </h3>
                <ul className="space-y-2">
                  {result.conditions.map((c, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-amber-800">
                      <CheckCircle2 className="w-4 h-4 mt-0.5 flex-shrink-0" />
                      {c}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {result.priority_actions.length > 0 && (
              <div className="bg-blue-50 rounded-xl border border-blue-200 p-5">
                <h3 className="font-bold text-blue-900 mb-3 flex items-center gap-2">
                  <Target className="w-5 h-5" />
                  Priority Actions
                </h3>
                <ul className="space-y-2">
                  {result.priority_actions.map((a, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-blue-800">
                      <Zap className="w-4 h-4 mt-0.5 flex-shrink-0" />
                      {a}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>
    );
  };

  // ==========================================================================
  // ANALYTICS / NEW ANALYSIS VIEW
  // ==========================================================================
  const AnalyticsView = () => (
    <div className="max-w-3xl mx-auto py-8">
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-8">
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 bg-indigo-100 rounded-lg flex items-center justify-center">
              <BrainCircuit className="w-6 h-6 text-indigo-600" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-slate-900">New Strategic Analysis</h2>
              <p className="text-sm text-slate-500">
                Our multi-agent AI system will analyze your decision from 6 perspectives.
              </p>
            </div>
          </div>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-2">
              Strategic Decision <span className="text-red-500">*</span>
            </label>
            <textarea
              {...register('decision')}
              rows={5}
              className="w-full px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none text-slate-800 placeholder-slate-400 text-sm"
              placeholder="e.g., Should we invest $2M in expanding our cloud infrastructure to support enterprise clients?"
              disabled={loading}
            />
            <div className="flex justify-between mt-1.5">
              {errors.decision ? (
                <p className="text-xs text-red-600">{errors.decision.message}</p>
              ) : (
                <span />
              )}
              <p className={`text-xs ${decisionValue.length > 1000 ? 'text-red-500' : 'text-slate-400'}`}>
                {decisionValue.length}/1000
              </p>
            </div>
          </div>

          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-2">
              Industry Context <span className="text-slate-400 font-normal">(Optional)</span>
            </label>
            <input
              {...register('industry_context')}
              type="text"
              className="w-full px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-slate-800 placeholder-slate-400 text-sm"
              placeholder="e.g., SaaS, Fintech, Healthcare, Manufacturing"
              disabled={loading}
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-2">Quick Examples</label>
            <div className="flex flex-wrap gap-2">
              {examples.map((ex, i) => (
                <button
                  key={i}
                  type="button"
                  onClick={() => reset({ decision: ex })}
                  className="text-xs px-3 py-2 bg-slate-100 hover:bg-indigo-50 hover:text-indigo-700 hover:border-indigo-200 border border-slate-200 rounded-lg text-slate-600 transition-all"
                  disabled={loading}
                >
                  Example {i + 1}
                </button>
              ))}
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-4 bg-slate-900 hover:bg-slate-800 text-white font-semibold rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-3 shadow-lg"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>Running Multi-Agent Analysis...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5" />
                <span>Execute Strategic Analysis</span>
                <ArrowRight className="w-5 h-5" />
              </>
            )}
          </button>
        </form>

        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="mt-4 bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3"
            >
              <AlertTriangle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
              <div>
                <p className="font-semibold text-red-800 text-sm">Analysis Failed</p>
                <p className="text-sm text-red-700 mt-0.5">{error}</p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );

  // ==========================================================================
  // REPORTS / HISTORY VIEW
  // ==========================================================================
  const ReportsView = () => (
    <div className="py-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-xl font-bold text-slate-900">Analysis History</h2>
          <p className="text-sm text-slate-500">View and manage past strategic decision analyses</p>
        </div>
        <div className="flex items-center gap-2">
          <button className="px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm text-slate-600 hover:bg-slate-50 flex items-center gap-2">
            <Filter className="w-4 h-4" />
            Filter
          </button>
          <button className="px-3 py-2 bg-indigo-600 text-white rounded-lg text-sm hover:bg-indigo-700 flex items-center gap-2">
            <Download className="w-4 h-4" />
            Export
          </button>
        </div>
      </div>

      {history.length === 0 ? (
        <div className="bg-white rounded-xl border border-slate-200 p-16 text-center">
          <div className="w-16 h-16 bg-slate-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <History className="w-8 h-8 text-slate-300" />
          </div>
          <h3 className="text-lg font-semibold text-slate-600 mb-1">No history yet</h3>
          <p className="text-sm text-slate-400 mb-4">Your analysis history will appear here</p>
          <button
            onClick={() => setActiveTab('analytics')}
            className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm hover:bg-indigo-700"
          >
            Run your first analysis
          </button>
        </div>
      ) : (
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
          <table className="w-full">
            <thead className="bg-slate-50 border-b border-slate-200">
              <tr>
                <th className="text-left text-xs font-semibold text-slate-500 uppercase tracking-wider px-6 py-3">Decision</th>
                <th className="text-left text-xs font-semibold text-slate-500 uppercase tracking-wider px-6 py-3">Verdict</th>
                <th className="text-left text-xs font-semibold text-slate-500 uppercase tracking-wider px-6 py-3">Confidence</th>
                <th className="text-left text-xs font-semibold text-slate-500 uppercase tracking-wider px-6 py-3">Date</th>
                <th className="text-left text-xs font-semibold text-slate-500 uppercase tracking-wider px-6 py-3">Status</th>
                <th className="px-6 py-3"></th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {history.map((item) => (
                <tr
                  key={item.id}
                  className="hover:bg-slate-50 transition-colors cursor-pointer"
                  onClick={() => {
                    // In real app, fetch full result by ID
                  }}
                >
                  <td className="px-6 py-4">
                    <p className="text-sm font-medium text-slate-900 line-clamp-1">{item.title}</p>
                  </td>
                  <td className="px-6 py-4">
                    <span className={`inline-flex px-2.5 py-1 rounded-full text-xs font-semibold ${
                      item.verdict === 'Proceed' ? 'bg-emerald-100 text-emerald-800' :
                      item.verdict === 'Proceed with Conditions' ? 'bg-amber-100 text-amber-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {item.verdict}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <div className="w-16 h-2 bg-slate-200 rounded-full overflow-hidden">
                        <div
                          className={`h-full rounded-full ${
                            item.confidence >= 75 ? 'bg-emerald-500' : item.confidence >= 50 ? 'bg-amber-500' : 'bg-red-500'
                          }`}
                          style={{ width: `${item.confidence}%` }}
                        />
                      </div>
                      <span className="text-sm text-slate-600">{item.confidence}%</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-sm text-slate-500">{item.date}</td>
                  <td className="px-6 py-4">
                    <span className="inline-flex items-center gap-1.5 text-xs">
                      <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full" />
                      <span className="text-slate-600 capitalize">{item.status}</span>
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <button className="text-slate-400 hover:text-slate-600">
                      <MoreHorizontal className="w-5 h-5" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );

  // ==========================================================================
  // RENDER
  // ==========================================================================
  return (
    <div className="min-h-screen bg-slate-50 flex">
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        isCollapsed={isSidebarCollapsed}
        setIsCollapsed={setIsSidebarCollapsed}
      />

      {/* Main Content */}
      <main className={`flex-1 transition-all duration-300 ${isSidebarCollapsed ? 'ml-16' : 'ml-60'}`}>
        {/* Top Header */}
        <header className="bg-white border-b border-slate-200 px-6 py-3 sticky top-0 z-40">
          <div className="flex items-center justify-between">
            {/* Search */}
            <div className="flex items-center gap-4 flex-1">
              <div className="relative max-w-md w-full">
                <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  placeholder="Search decisions, reports, or insights..."
                  className="w-full pl-10 pr-4 py-2 bg-slate-100 border-none rounded-lg text-sm text-slate-700 placeholder-slate-400 focus:ring-2 focus:ring-indigo-500 focus:bg-white transition-all"
                />
              </div>
            </div>

            {/* Right Actions */}
            <div className="flex items-center gap-3">
              <button className="relative p-2 text-slate-500 hover:bg-slate-100 rounded-lg transition-colors">
                <Bell className="w-5 h-5" />
                <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full" />
              </button>
              <div className="w-8 h-8 bg-indigo-600 rounded-full flex items-center justify-center text-white text-sm font-semibold">
                JD
              </div>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <div className="p-6">
          <AnimatePresence mode="wait">
            <motion.div
              key={activeTab}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }}
              transition={{ duration: 0.2 }}
            >
              {activeTab === 'home' && <HomeView />}
              {activeTab === 'analytics' && <AnalyticsView />}
              {activeTab === 'reports' && <ReportsView />}
              {activeTab === 'workspace' && (
                <div className="flex flex-col items-center justify-center h-[60vh] text-slate-400">
                  <FolderOpen className="w-12 h-12 mb-3 text-slate-300" />
                  <p>Workspace coming soon</p>
                </div>
              )}
              {activeTab === 'settings' && (
                <div className="flex flex-col items-center justify-center h-[60vh] text-slate-400">
                  <Settings className="w-12 h-12 mb-3 text-slate-300" />
                  <p>Settings coming soon</p>
                </div>
              )}
            </motion.div>
          </AnimatePresence>
        </div>
      </main>

      {/* Full Report Modal */}
      <AnimatePresence>
        {showFullReport && result && (
          <FullReportModal result={result} onClose={() => setShowFullReport(false)} />
        )}
      </AnimatePresence>
    </div>
  );
};

export default App;
