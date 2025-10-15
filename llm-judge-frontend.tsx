import React, { useState } from 'react';
import { Scale, ArrowRight, Check, X, AlertTriangle } from 'lucide-react';

export default function LLMJudgePlatform() {
  const [step, setStep] = useState(0);
  const [context, setContext] = useState({ domain: '' });
  const [criteria, setCriteria] = useState([]);
  const [selectedModel, setSelectedModel] = useState('');
  const [evaluating, setEvaluating] = useState(false);
  const [progress, setProgress] = useState(0);
  const [results, setResults] = useState(null);
  const [pdfFile, setPdfFile] = useState(null);
  const [error, setError] = useState(null);
  const [availableModels, setAvailableModels] = useState([]);
  const [errorDetails, setErrorDetails] = useState(null);
  const [requestLog, setRequestLog] = useState([]);

  // Backend API URL
  const API_BASE_URL = 'http://localhost:8000';

  // Helper to log requests
  const logRequest = (method, url, status, details) => {
    const timestamp = new Date().toISOString();
    const logEntry = { timestamp, method, url, status, details };
    console.log(`[${timestamp}] ${method} ${url} - Status: ${status}`, details);
    setRequestLog(prev => [...prev, logEntry].slice(-10)); // Keep last 10
  };

  const suggestCriteria = (domain) => {
    const criteriaMap = {
      legal: [
        { name: 'CITATION_ACCURACY', weight: 40, hardMin: 90 },
        { name: 'LEGAL_REASONING', weight: 30, hardMin: 80 },
        { name: 'JURISDICTION', weight: 20, hardMin: 85 },
        { name: 'FABRICATION_DETECT', weight: 10, hardMin: 95 }
      ],
      medical: [
        { name: 'MEDICAL_ACCURACY', weight: 50, hardMin: 95 },
        { name: 'SAFETY_CHECK', weight: 30, hardMin: 90 },
        { name: 'EVIDENCE_BASED', weight: 15, hardMin: 85 },
        { name: 'CLARITY', weight: 5, hardMin: 70 }
      ],
      finance: [
        { name: 'DATA_ACCURACY', weight: 45, hardMin: 95 },
        { name: 'COMPLIANCE', weight: 30, hardMin: 90 },
        { name: 'RISK_DISCLOSURE', weight: 15, hardMin: 85 },
        { name: 'REASONING', weight: 10, hardMin: 75 }
      ]
    };
    return criteriaMap[domain] || criteriaMap.legal;
  };

  // Fetch available models on component mount
  React.useEffect(() => {
    fetchAvailableModels();
  }, []);

  const fetchAvailableModels = async () => {
    const url = `${API_BASE_URL}/api/models`;
    try {
      console.log('[API] Fetching available models from:', url);
      const response = await fetch(url);
      
      logRequest('GET', url, response.status, { ok: response.ok });
      
      if (response.ok) {
        const data = await response.json();
        console.log('[API] Models fetched successfully:', data.models);
        setAvailableModels(data.models);
      } else {
        const errorText = await response.text();
        console.error('[API] Failed to fetch models:', response.status, errorText);
      }
    } catch (err) {
      console.error('[API] Network error fetching models:', err);
      logRequest('GET', url, 0, { error: err.message || String(err) });
    }
  };

  const runEvaluation = async () => {
    if (!pdfFile) {
      setError('Please upload a PDF file');
      return;
    }

    setEvaluating(true);
    setProgress(0);
    setError(null);
    setErrorDetails(null);

    const url = `${API_BASE_URL}/api/evaluate`;

    try {
      // Create FormData for file upload
      const formData = new FormData();
      formData.append('file', pdfFile);
      formData.append('criteria', JSON.stringify(criteria));
      
      // Map frontend model names to backend model names
      const modelMap = {
        'CLAUDE_SONNET_4.5': 'claude-sonnet-4',
        'GPT-4O': 'gpt-4o',
        'GPT-4O-MINI': 'gpt-4o-mini'
      };
      const backendModel = modelMap[selectedModel] || 'claude-sonnet-4';
      formData.append('judge_model', backendModel);

      console.log('[API] Starting evaluation:', {
        file: pdfFile.name,
        size: pdfFile.size,
        criteria: criteria,
        model: backendModel,
        url: url
      });

      // Simulate progress while waiting for API
      const progressInterval = setInterval(() => {
        setProgress(prev => Math.min(prev + 10, 90));
      }, 500);

      // Call backend API
      const startTime = Date.now();
      const response = await fetch(url, {
        method: 'POST',
        body: formData,
      });
      const duration = Date.now() - startTime;

      clearInterval(progressInterval);
      setProgress(100);

      console.log(`[API] Response received in ${duration}ms:`, {
        status: response.status,
        statusText: response.statusText,
        headers: Object.fromEntries(response.headers.entries())
      });

      logRequest('POST', url, response.status, { 
        duration: `${duration}ms`,
        ok: response.ok 
      });

      if (!response.ok) {
        let errorData;
        const contentType = response.headers.get('content-type');
        
        if (contentType && contentType.includes('application/json')) {
          errorData = await response.json();
          console.error('[API] Error response:', errorData);
        } else {
          const errorText = await response.text();
          console.error('[API] Error response (text):', errorText);
          errorData = { detail: errorText };
        }
        
        setErrorDetails({
          status: response.status,
          statusText: response.statusText,
          message: errorData.detail || errorData.message || 'Unknown error',
          data: errorData
        });
        
        throw new Error(errorData.detail || errorData.message || `HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      console.log('[API] Evaluation completed successfully:', data);
      
      // Transform backend response to frontend format
      const transformedResults = {
        evaluations: data.evaluations.map((evaluation, idx) => ({
          id: evaluation.qa_id || idx + 1,
          verdict: evaluation.verdict,
          score: Math.round(evaluation.weighted_score),
          details: evaluation.scores
        })),
        summary: {
          total: data.summary.total_evaluated || 0,
          passed: data.summary.passed || 0,
          failed: data.summary.failed || 0,
          avgScore: Math.round(data.summary.average_score || 0)
        }
      };

      console.log('[API] Results transformed:', transformedResults);
      setResults(transformedResults);
      setStep(4);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to evaluate. Make sure the backend is running.';
      setError(errorMessage);
      
      console.error('[API] Evaluation error:', {
        error: err,
        message: errorMessage,
        type: err?.constructor?.name,
        stack: err instanceof Error ? err.stack : undefined
      });
      
      logRequest('POST', url, 0, { 
        error: errorMessage,
        type: 'catch'
      });
      
      if (!errorDetails) {
        setErrorDetails({
          status: 0,
          statusText: 'Network Error',
          message: errorMessage,
          data: err
        });
      }
    } finally {
      setEvaluating(false);
    }
  };

  // SVG Hand-drawn elements
  const SketchyBox = ({ children, className = "" }) => (
    <div className={`relative ${className}`}>
      <svg className="absolute inset-0 w-full h-full pointer-events-none" style={{ filter: 'url(#roughen)' }}>
        <defs>
          <filter id="roughen">
            <feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="2" result="noise" />
            <feDisplacementMap in="SourceGraphic" in2="noise" scale="2" />
          </filter>
        </defs>
        <rect x="4" y="4" width="calc(100% - 8px)" height="calc(100% - 8px)" 
              fill="none" stroke="currentColor" strokeWidth="2"
              strokeDasharray="5,5" />
      </svg>
      <div className="relative p-6">
        {children}
      </div>
    </div>
  );

  const GridBackground = () => (
    <div className="fixed inset-0 pointer-events-none opacity-20">
      <svg width="100%" height="100%">
        <defs>
          <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
            <path d="M 20 0 L 0 0 0 20" fill="none" stroke="currentColor" strokeWidth="0.5"/>
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#grid)" />
      </svg>
    </div>
  );

  // Hero Section
  const HeroSection = () => (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6 relative">
      <GridBackground />
      
      <div className="max-w-4xl mx-auto text-center relative z-10">
        {/* Hand-drawn title box */}
        <div className="mb-12 relative">
          <svg className="absolute inset-0 w-full h-full" style={{ filter: 'url(#roughen)' }}>
            <rect x="10" y="10" width="calc(100% - 20px)" height="calc(100% - 20px)" 
                  fill="none" stroke="#000" strokeWidth="3" />
          </svg>
          <div className="relative p-12">
            <div className="inline-block mb-4">
              <Scale className="w-16 h-16" strokeWidth={2.5} />
            </div>
            <h1 className="text-7xl md:text-8xl font-black mb-4 tracking-tight uppercase">
              LLM_JUDGE
            </h1>
            <div className="w-32 h-1 bg-black mx-auto mb-4"></div>
            <p className="text-xl font-mono uppercase tracking-wider">
              DOCUMENT-GROUNDED_EVALUATION
            </p>
          </div>
        </div>

        <div className="mb-12">
          <p className="text-2xl font-bold mb-2 uppercase">CATCHES HALLUCINATIONS</p>
          <p className="text-lg text-gray-600 font-mono">
            [BEFORE_THEY_CATCH_YOU]
          </p>
        </div>

        <button
          onClick={() => setStep(1)}
          className="group relative inline-flex items-center gap-3 px-12 py-6 bg-black text-white text-xl font-black uppercase hover:bg-gray-900 transition-all"
        >
          <span>[START_EVAL]</span>
          <ArrowRight className="w-6 h-6 group-hover:translate-x-1 transition-transform" />
          <svg className="absolute inset-0 w-full h-full pointer-events-none">
            <rect x="2" y="2" width="calc(100% - 4px)" height="calc(100% - 4px)" 
                  fill="none" stroke="white" strokeWidth="2" opacity="0.3" />
          </svg>
        </button>

        {/* Stats grid */}
        <div className="mt-20 grid grid-cols-3 gap-8 max-w-3xl mx-auto">
          {[
            { label: 'DETECTION_RATE', value: '95%' },
            { label: 'LATENCY', value: '<100ms' },
            { label: 'COST_SAVE', value: '85%' }
          ].map((stat, idx) => (
            <div key={idx} className="relative">
              <SketchyBox>
                <div className="text-4xl font-black mb-2">{stat.value}</div>
                <div className="text-xs font-mono uppercase">{stat.label}</div>
              </SketchyBox>
            </div>
          ))}
        </div>

        <div className="mt-12 text-sm font-mono text-gray-500">
          // BUILT_OVERNIGHT_WITH_FOCUS
        </div>
      </div>
    </div>
  );

  // Domain Selection
  const DomainSelection = () => (
    <div className="min-h-screen bg-gray-50 py-20 px-6 relative">
      <GridBackground />
      
      <div className="max-w-5xl mx-auto relative z-10">
        <div className="text-center mb-16">
          <div className="inline-block px-6 py-2 border-2 border-black mb-6">
            <span className="font-mono text-sm">[01/03]</span>
          </div>
          <h2 className="text-6xl font-black mb-4 uppercase tracking-tight">
            SELECT_DOMAIN
          </h2>
          <p className="text-lg font-mono text-gray-600">
            // EACH_HAS_UNIQUE_FAILURE_MODES
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 mb-12">
          {[
            { id: 'legal', name: 'LEGAL', stat: '69%_ERROR', issue: 'CITATION_FABRICATION' },
            { id: 'medical', name: 'MEDICAL', stat: '34%_ERROR', issue: 'TREATMENT_HALLUC' },
            { id: 'finance', name: 'FINANCE', stat: 'ZERO_TOLERANCE', issue: 'DATA_ACCURACY' }
          ].map((domain) => (
            <button
              key={domain.id}
              onClick={() => {
                setContext({...context, domain: domain.id});
                setCriteria(suggestCriteria(domain.id));
              }}
              className={`relative p-8 text-left transition-all hover:scale-105 ${
                context.domain === domain.id ? 'bg-black text-white' : 'bg-white'
              }`}
            >
              <svg className="absolute inset-0 w-full h-full pointer-events-none">
                <rect x="4" y="4" width="calc(100% - 8px)" height="calc(100% - 8px)" 
                      fill="none" stroke="currentColor" strokeWidth="3" />
              </svg>
              <div className="relative">
                <h3 className="text-3xl font-black mb-6 uppercase">{domain.name}</h3>
                <div className="space-y-2 font-mono text-sm">
                  <div>ERROR_RATE: {domain.stat}</div>
                  <div>ISSUE: {domain.issue}</div>
                </div>
                {context.domain === domain.id && (
                  <div className="absolute top-0 right-0">
                    <Check className="w-8 h-8" />
                  </div>
                )}
              </div>
            </button>
          ))}
        </div>

        {context.domain && (
          <div className="text-center">
            <button
              onClick={() => setStep(2)}
              className="px-12 py-4 bg-black text-white font-black uppercase hover:bg-gray-900 transition-all inline-flex items-center gap-3"
            >
              CONTINUE
              <ArrowRight className="w-5 h-5" />
            </button>
          </div>
        )}
      </div>
    </div>
  );

  // Criteria Selection
  const CriteriaSelection = () => (
    <div className="min-h-screen bg-gray-50 py-20 px-6 relative">
      <GridBackground />
      
      <div className="max-w-4xl mx-auto relative z-10">
        <div className="text-center mb-16">
          <div className="inline-block px-6 py-2 border-2 border-black mb-6">
            <span className="font-mono text-sm">[02/03]</span>
          </div>
          <h2 className="text-6xl font-black mb-4 uppercase tracking-tight">
            EVALUATION_CRITERIA
          </h2>
          <p className="text-lg font-mono text-gray-600">
            // WEIGHTED_WITH_HARD_MINIMUMS
          </p>
        </div>

        <div className="space-y-6 mb-12">
          {criteria.map((criterion, idx) => (
            <div key={idx} className="relative bg-white p-6">
              <svg className="absolute inset-0 w-full h-full pointer-events-none">
                <rect x="2" y="2" width="calc(100% - 4px)" height="calc(100% - 4px)" 
                      fill="none" stroke="black" strokeWidth="2" />
              </svg>
              <div className="relative flex items-center justify-between">
                <div className="flex-1">
                  <div className="font-black text-xl mb-2 uppercase font-mono">
                    {criterion.name}
                  </div>
                  <div className="text-sm text-gray-600 font-mono">
                    HARD_MIN: {criterion.hardMin}%
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-5xl font-black">{criterion.weight}%</div>
                  <div className="text-xs font-mono text-gray-600">WEIGHT</div>
                </div>
              </div>
              <div className="mt-4 h-2 bg-gray-200 relative">
                <div 
                  className="absolute top-0 left-0 h-full bg-black transition-all"
                  style={{ width: `${criterion.weight}%` }}
                />
              </div>
            </div>
          ))}
        </div>

        <div className="relative bg-black text-white p-8 mb-12">
          <svg className="absolute inset-0 w-full h-full pointer-events-none">
            <rect x="4" y="4" width="calc(100% - 8px)" height="calc(100% - 8px)" 
                  fill="none" stroke="white" strokeWidth="2" opacity="0.3" />
          </svg>
          <div className="relative flex items-center justify-between">
            <div>
              <div className="text-sm font-mono mb-2">GLOBAL_THRESHOLD</div>
              <div className="text-lg">WEIGHTED_AVERAGE_MUST_EXCEED</div>
            </div>
            <div className="text-7xl font-black">85</div>
          </div>
        </div>

        <div className="flex gap-4 justify-center">
          <button
            onClick={() => setStep(1)}
            className="px-8 py-4 border-2 border-black font-black uppercase hover:bg-black hover:text-white transition-all"
          >
            BACK
          </button>
          <button
            onClick={() => setStep(3)}
            className="px-12 py-4 bg-black text-white font-black uppercase hover:bg-gray-900 transition-all inline-flex items-center gap-3"
          >
            SELECT_MODEL
            <ArrowRight className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );

  // Model Selection
  const ModelSelection = () => (
    <div className="min-h-screen bg-gray-50 py-20 px-6 relative">
      <GridBackground />
      
      <div className="max-w-5xl mx-auto relative z-10">
        <div className="text-center mb-16">
          <div className="inline-block px-6 py-2 border-2 border-black mb-6">
            <span className="font-mono text-sm">[03/03]</span>
          </div>
          <h2 className="text-6xl font-black mb-4 uppercase tracking-tight">
            JUDGE_MODEL
          </h2>
          <p className="text-lg font-mono text-gray-600">
            // SELECT_EVALUATION_ENGINE
          </p>
        </div>

        {/* PDF Upload Section */}
        <div className="mb-12 relative bg-white p-8">
          <svg className="absolute inset-0 w-full h-full pointer-events-none">
            <rect x="3" y="3" width="calc(100% - 6px)" height="calc(100% - 6px)" 
                  fill="none" stroke="black" strokeWidth="2" strokeDasharray="10,5" />
          </svg>
          <div className="relative">
            <label className="block text-2xl font-black mb-4 uppercase">
              UPLOAD_PDF_DOCUMENT
            </label>
            <input
              type="file"
              accept="application/pdf"
              onChange={(e) => setPdfFile(e.target.files?.[0] || null)}
              className="block w-full text-sm font-mono border-2 border-black p-4 cursor-pointer
                       file:mr-4 file:py-2 file:px-4
                       file:border-0 file:text-sm file:font-black
                       file:bg-black file:text-white
                       hover:file:bg-gray-900"
            />
            {pdfFile && (
              <div className="mt-4 text-sm font-mono text-green-600">
                ✓ FILE_SELECTED: {pdfFile.name}
              </div>
            )}
            {error && (
              <div className="mt-4 p-4 bg-red-100 border-2 border-red-600 text-red-900 font-mono text-sm">
                <div className="font-black mb-2">❌ ERROR:</div>
                <div className="mb-3">{error}</div>
                
                {errorDetails && (
                  <details className="mt-3 cursor-pointer">
                    <summary className="font-black hover:underline">View Technical Details</summary>
                    <div className="mt-2 p-3 bg-red-200 border border-red-700 text-xs overflow-auto max-h-64">
                      <div><strong>Status:</strong> {errorDetails.status} {errorDetails.statusText}</div>
                      <div className="mt-2"><strong>Message:</strong> {errorDetails.message}</div>
                      {errorDetails.data && (
                        <div className="mt-2">
                          <strong>Details:</strong>
                          <pre className="mt-1 whitespace-pre-wrap">{JSON.stringify(errorDetails.data, null, 2)}</pre>
                        </div>
                      )}
                    </div>
                  </details>
                )}
                
                <div className="mt-3 pt-3 border-t border-red-700">
                  <div className="font-black mb-1">💡 Troubleshooting:</div>
                  <ul className="list-disc list-inside text-xs space-y-1">
                    <li>Make sure backend is running: <code className="bg-red-200 px-1">uvicorn app.main:app --reload</code></li>
                    <li>Check backend health: <code className="bg-red-200 px-1">curl http://localhost:8000/api/health</code></li>
                    <li>Open browser console (F12) for detailed logs</li>
                  </ul>
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="space-y-6 mb-12">
          {[
            {
              name: 'CLAUDE_SONNET_4.5',
              speed: 'FAST',
              cost: '$0.05',
              accuracy: '95%',
              recommended: true
            },
            {
              name: 'GPT-4O',
              speed: 'VERY_FAST',
              cost: '$0.04',
              accuracy: '92%',
            },
            {
              name: 'GPT-4O-MINI',
              speed: 'FASTEST',
              cost: '$0.01',
              accuracy: '85%',
            }
          ].map((model, idx) => (
            <button
              key={idx}
              onClick={() => setSelectedModel(model.name)}
              className={`w-full p-8 text-left transition-all hover:scale-105 relative ${
                selectedModel === model.name ? 'bg-black text-white' : 'bg-white'
              }`}
            >
              <svg className="absolute inset-0 w-full h-full pointer-events-none">
                <rect x="3" y="3" width="calc(100% - 6px)" height="calc(100% - 6px)" 
                      fill="none" stroke="currentColor" strokeWidth="3" />
              </svg>
              <div className="relative">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-3xl font-black uppercase font-mono">{model.name}</h3>
                  {model.recommended && (
                    <div className="px-4 py-1 border-2 border-current text-sm font-black">
                      RECOMMENDED
                    </div>
                  )}
                </div>
                
                <div className="grid grid-cols-3 gap-6 font-mono text-sm">
                  <div>
                    <div className="text-3xl font-black mb-1">{model.accuracy}</div>
                    <div className="opacity-60">ACCURACY</div>
                  </div>
                  <div>
                    <div className="text-3xl font-black mb-1">{model.cost}</div>
                    <div className="opacity-60">PER_EVAL</div>
                  </div>
                  <div>
                    <div className="text-xl font-black mb-1">{model.speed}</div>
                    <div className="opacity-60">SPEED</div>
                  </div>
                </div>

                {selectedModel === model.name && (
                  <div className="absolute top-8 right-8">
                    <Check className="w-10 h-10" />
                  </div>
                )}
              </div>
            </button>
          ))}
        </div>

        {selectedModel && pdfFile && (
          <div className="text-center">
            <button
              onClick={runEvaluation}
              disabled={!pdfFile}
              className="px-16 py-6 bg-black text-white text-xl font-black uppercase hover:bg-gray-900 transition-all inline-flex items-center gap-4 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              RUN_EVALUATION
              <ArrowRight className="w-6 h-6" />
            </button>
          </div>
        )}
        
        {selectedModel && !pdfFile && (
          <div className="text-center p-4 bg-yellow-100 border-2 border-yellow-600 font-mono">
            ⚠ PLEASE_UPLOAD_PDF_FIRST
          </div>
        )}
      </div>
    </div>
  );

  // Evaluating
  const EvaluatingScreen = () => (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6 relative">
      <GridBackground />
      
      <div className="text-center max-w-2xl mx-auto relative z-10">
        <div className="mb-12">
          <div className="w-32 h-32 mx-auto mb-8 relative">
            <div className="absolute inset-0 border-4 border-black animate-spin" style={{ borderRadius: '50%' }} />
            <div className="absolute inset-4 flex items-center justify-center">
              <Scale className="w-16 h-16" />
            </div>
          </div>
          
          <h2 className="text-5xl font-black mb-4 uppercase">ANALYZING...</h2>
          <p className="text-lg font-mono text-gray-600">
            // RUNNING_{selectedModel}
          </p>
        </div>

        <div className="mb-12">
          <div className="h-4 bg-white border-2 border-black mb-4 relative overflow-hidden">
            <div 
              className="absolute inset-0 bg-black transition-all"
              style={{ width: `${progress}%` }}
            />
          </div>
          <div className="text-7xl font-black tabular-nums">{Math.round(progress)}%</div>
        </div>

        <div className="grid grid-cols-3 gap-6">
          <SketchyBox>
            <div className="text-4xl font-black text-green-600 mb-2">1</div>
            <div className="text-xs font-mono">PASSED</div>
          </SketchyBox>
          <SketchyBox>
            <div className="text-4xl font-black text-red-600 mb-2">2</div>
            <div className="text-xs font-mono">FAILED</div>
          </SketchyBox>
          <SketchyBox>
            <div className="text-4xl font-black mb-2">0</div>
            <div className="text-xs font-mono">PENDING</div>
          </SketchyBox>
        </div>
      </div>
    </div>
  );

  // Results
  const ResultsScreen = () => (
    <div className="min-h-screen bg-gray-50 py-20 px-6 relative">
      <GridBackground />
      
      <div className="max-w-5xl mx-auto relative z-10">
        <div className="text-center mb-16">
          <div className="inline-block w-24 h-24 border-4 border-red-600 flex items-center justify-center mb-6">
            <AlertTriangle className="w-12 h-12 text-red-600" />
          </div>
          <h2 className="text-6xl font-black mb-4 uppercase">
            {results.summary.failed > 0 ? 'ISSUES_DETECTED' : 'ALL_PASSED'}
          </h2>
          <p className="text-2xl font-mono">
            {results.summary.passed}_OF_{results.summary.total}_PASSED
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6 mb-16">
          <SketchyBox className="bg-white">
            <div className="text-5xl font-black mb-2">
              {results.summary.total > 0 
                ? Math.round((results.summary.passed / results.summary.total) * 100) 
                : 0}%
            </div>
            <div className="text-sm font-mono">PASS_RATE</div>
          </SketchyBox>
          <SketchyBox className="bg-white">
            <div className="text-5xl font-black text-red-600 mb-2">
              {results.summary.total > 0 
                ? Math.round((results.summary.failed / results.summary.total) * 100) 
                : 0}%
            </div>
            <div className="text-sm font-mono">FAIL_RATE</div>
          </SketchyBox>
          <SketchyBox className="bg-white">
            <div className="text-5xl font-black mb-2">{results.summary.avgScore || 0}</div>
            <div className="text-sm font-mono">AVG_SCORE</div>
          </SketchyBox>
        </div>

        <div className="space-y-6 mb-12">
          {results.evaluations.map((result, idx) => (
            <div
              key={idx}
              className={`relative p-8 ${
                result.verdict === 'PASS' ? 'bg-green-100' : 'bg-red-100'
              }`}
            >
              <svg className="absolute inset-0 w-full h-full pointer-events-none">
                <rect x="4" y="4" width="calc(100% - 8px)" height="calc(100% - 8px)" 
                      fill="none" stroke="black" strokeWidth="3" />
              </svg>
              <div className="relative">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-6">
                    {result.verdict === 'PASS' ? (
                      <Check className="w-12 h-12" />
                    ) : (
                      <X className="w-12 h-12" />
                    )}
                    <div>
                      <div className="text-2xl font-black mb-2 uppercase font-mono">
                        QUESTION_{result.id}
                      </div>
                      <div className="text-sm font-mono text-gray-700">
                        STATUS: {result.verdict}
                      </div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-6xl font-black">{result.score}</div>
                    <div className="text-sm font-mono">SCORE</div>
                  </div>
                </div>
                
                {/* Show criterion details */}
                {result.details && (
                  <div className="mt-4 pt-4 border-t-2 border-black/20 space-y-2">
                    {Object.entries(result.details).map(([criterionName, criterionData]: [string, any]) => (
                      <div key={criterionName} className="flex justify-between items-center text-sm font-mono">
                        <span>{criterionName}:</span>
                        <span className={criterionData.passed ? 'text-green-700' : 'text-red-700'}>
                          {criterionData.score}/100 {criterionData.passed ? '✓' : '✗'}
                        </span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        <div className="flex gap-4 justify-center">
          <button
            onClick={() => {
              setStep(0);
              setResults(null);
              setContext({ domain: '' });
            }}
            className="px-10 py-5 border-2 border-black font-black uppercase hover:bg-black hover:text-white transition-all"
          >
            NEW_EVAL
          </button>
          <button className="px-10 py-5 bg-black text-white font-black uppercase hover:bg-gray-900 transition-all">
            DOWNLOAD_REPORT
          </button>
        </div>
      </div>
    </div>
  );

  return (
    <div className="font-sans antialiased">
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&family=Space+Mono:wght@400;700&display=swap');
        * { 
          font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        .font-mono {
          font-family: 'Space Mono', monospace;
        }
      `}</style>
      
      {step === 0 && <HeroSection />}
      {step === 1 && <DomainSelection />}
      {step === 2 && <CriteriaSelection />}
      {step === 3 && <ModelSelection />}
      {evaluating && <EvaluatingScreen />}
      {step === 4 && !evaluating && <ResultsScreen />}
      
      {/* Debug Panel - Request Log */}
      {requestLog.length > 0 && (
        <div className="fixed bottom-4 right-4 w-96 max-h-64 bg-black text-green-400 font-mono text-xs p-4 overflow-auto shadow-lg z-50 border-2 border-green-500">
          <div className="flex justify-between items-center mb-2 pb-2 border-b border-green-500">
            <span className="font-black">🔍 API REQUEST LOG</span>
            <button 
              onClick={() => setRequestLog([])}
              className="text-red-400 hover:text-red-300 font-black"
            >
              [CLEAR]
            </button>
          </div>
          <div className="space-y-2">
            {requestLog.map((log, idx) => (
              <div key={idx} className="pb-2 border-b border-green-900">
                <div className="flex justify-between">
                  <span className="text-yellow-400">{log.method}</span>
                  <span className={log.status >= 200 && log.status < 300 ? 'text-green-400' : 'text-red-400'}>
                    {log.status || 'ERR'}
                  </span>
                </div>
                <div className="text-gray-400 truncate">{log.url}</div>
                <div className="text-gray-500 text-xxs">{new Date(log.timestamp).toLocaleTimeString()}</div>
                {log.details && (
                  <details className="mt-1">
                    <summary className="cursor-pointer hover:text-white">Details</summary>
                    <pre className="mt-1 text-xxs whitespace-pre-wrap">{JSON.stringify(log.details, null, 2)}</pre>
                  </details>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}