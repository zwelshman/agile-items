"use client";

import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Sparkles,
  Zap,
  Download,
  Copy,
  Check,
  ArrowRight,
  Loader2,
  Lightbulb,
  Target,
  ListChecks,
  Code2,
  ClipboardList,
  Scale,
  ChevronDown,
  Settings,
  RefreshCw,
} from "lucide-react";
import ReactMarkdown from "react-markdown";

// Example work items for inspiration
const exampleItems = [
  "Fix the slow dashboard",
  "Add dark mode to settings",
  "Users need to export data as CSV",
  "Login page is confusing",
  "The search doesn't work well",
  "Add notification system",
];

// Animated background particles
function Particles() {
  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none">
      {[...Array(20)].map((_, i) => (
        <motion.div
          key={i}
          className="absolute w-1 h-1 bg-violet-500/30 rounded-full"
          initial={{
            x: Math.random() * (typeof window !== "undefined" ? window.innerWidth : 1000),
            y: typeof window !== "undefined" ? window.innerHeight + 10 : 1000,
          }}
          animate={{
            y: -10,
            x: `+=${Math.sin(i) * 100}`,
          }}
          transition={{
            duration: 15 + Math.random() * 10,
            repeat: Infinity,
            delay: Math.random() * 10,
            ease: "linear",
          }}
        />
      ))}
    </div>
  );
}

// Feature card component
function FeatureCard({
  icon: Icon,
  title,
  description,
  delay,
}: {
  icon: React.ElementType;
  title: string;
  description: string;
  delay: number;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.5 }}
      className="glass rounded-xl p-4 glass-hover transition-all duration-300"
    >
      <div className="flex items-start gap-3">
        <div className="p-2 rounded-lg bg-violet-500/20">
          <Icon className="w-5 h-5 text-violet-400" />
        </div>
        <div>
          <h3 className="font-semibold text-white text-sm">{title}</h3>
          <p className="text-xs text-gray-400 mt-1">{description}</p>
        </div>
      </div>
    </motion.div>
  );
}

// Main component
export default function Home() {
  const [input, setInput] = useState("");
  const [context, setContext] = useState("");
  const [output, setOutput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const [showContext, setShowContext] = useState(false);
  const [currentExample, setCurrentExample] = useState(0);
  const outputRef = useRef<HTMLDivElement>(null);

  // Cycle through examples
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentExample((prev) => (prev + 1) % exampleItems.length);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  // Generate agile description
  const handleGenerate = async () => {
    if (!input.trim()) return;

    setIsLoading(true);
    setOutput("");

    try {
      const response = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ workItem: input, teamContext: context }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || "Failed to generate");
      }

      const data = await response.json();
      setOutput(data.result);

      // Scroll to output
      setTimeout(() => {
        outputRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
      }, 100);
    } catch (error) {
      setOutput(
        `## Error\n\nFailed to generate description. ${error instanceof Error ? error.message : "Please try again."}`
      );
    } finally {
      setIsLoading(false);
    }
  };

  // Copy to clipboard
  const handleCopy = async () => {
    await navigator.clipboard.writeText(output);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // Download as markdown
  const handleDownload = () => {
    const blob = new Blob([output], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "agile-work-item.md";
    a.click();
    URL.revokeObjectURL(url);
  };

  // Clear all
  const handleClear = () => {
    setInput("");
    setContext("");
    setOutput("");
  };

  return (
    <main className="min-h-screen gradient-bg relative overflow-hidden">
      <Particles />

      {/* Hero Section */}
      <div className="relative z-10">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pt-16 pb-8">
          {/* Logo/Header */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center mb-12"
          >
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass mb-6">
              <Sparkles className="w-4 h-4 text-violet-400" />
              <span className="text-sm text-gray-300">Powered by Claude AI</span>
            </div>

            <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold mb-4">
              <span className="text-gradient-animated">Agile Refinery</span>
            </h1>

            <p className="text-xl text-gray-400 max-w-2xl mx-auto">
              Transform rough ideas into polished, actionable work items in seconds
            </p>
          </motion.div>

          {/* Main Card */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2, duration: 0.5 }}
            className="glass rounded-2xl p-6 sm:p-8 glow-purple"
          >
            {/* Input Section */}
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <label className="text-sm font-medium text-gray-300 flex items-center gap-2">
                  <Lightbulb className="w-4 h-4 text-yellow-400" />
                  Your Work Item
                </label>
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setInput(exampleItems[currentExample])}
                  className="text-xs text-violet-400 hover:text-violet-300 flex items-center gap-1"
                >
                  Try example <ArrowRight className="w-3 h-3" />
                </motion.button>
              </div>

              <div className="relative">
                <textarea
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder={`e.g., "${exampleItems[currentExample]}"`}
                  rows={4}
                  className="w-full bg-black/30 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:border-violet-500/50 focus:ring-2 focus:ring-violet-500/20 transition-all resize-none"
                />
                <AnimatePresence>
                  {input && (
                    <motion.div
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      exit={{ opacity: 0, scale: 0.8 }}
                      className="absolute right-3 top-3"
                    >
                      <span className="text-xs text-gray-500">{input.length} chars</span>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>

              {/* Team Context Accordion */}
              <div className="border border-white/5 rounded-xl overflow-hidden">
                <button
                  onClick={() => setShowContext(!showContext)}
                  className="w-full flex items-center justify-between px-4 py-3 hover:bg-white/5 transition-colors"
                >
                  <span className="text-sm text-gray-400 flex items-center gap-2">
                    <Settings className="w-4 h-4" />
                    Team Context (Optional)
                  </span>
                  <motion.div
                    animate={{ rotate: showContext ? 180 : 0 }}
                    transition={{ duration: 0.2 }}
                  >
                    <ChevronDown className="w-4 h-4 text-gray-500" />
                  </motion.div>
                </button>
                <AnimatePresence>
                  {showContext && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: "auto", opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.2 }}
                    >
                      <div className="px-4 pb-4">
                        <textarea
                          value={context}
                          onChange={(e) => setContext(e.target.value)}
                          placeholder="Add context about your team, project, or domain-specific terminology..."
                          rows={3}
                          className="w-full bg-black/20 border border-white/5 rounded-lg px-3 py-2 text-sm text-white placeholder-gray-600 focus:border-violet-500/30 focus:ring-1 focus:ring-violet-500/10 transition-all resize-none"
                        />
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>

              {/* Action Buttons */}
              <div className="flex gap-3 pt-2">
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={handleGenerate}
                  disabled={!input.trim() || isLoading}
                  className="flex-1 bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-500 hover:to-purple-500 disabled:from-gray-600 disabled:to-gray-700 disabled:cursor-not-allowed text-white font-semibold py-3 px-6 rounded-xl transition-all btn-glow flex items-center justify-center gap-2"
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin" />
                      Refining...
                    </>
                  ) : (
                    <>
                      <Zap className="w-5 h-5" />
                      Refine Work Item
                    </>
                  )}
                </motion.button>
                {(input || output) && (
                  <motion.button
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={handleClear}
                    className="p-3 rounded-xl border border-white/10 hover:bg-white/5 transition-all"
                  >
                    <RefreshCw className="w-5 h-5 text-gray-400" />
                  </motion.button>
                )}
              </div>
            </div>
          </motion.div>

          {/* Features Grid */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
            className="grid grid-cols-2 lg:grid-cols-3 gap-3 mt-8"
          >
            <FeatureCard
              icon={Target}
              title="User Stories"
              description="Clear 'As a... I want...' format"
              delay={0.5}
            />
            <FeatureCard
              icon={ListChecks}
              title="Acceptance Criteria"
              description="3-5 testable conditions"
              delay={0.6}
            />
            <FeatureCard
              icon={Code2}
              title="Technical Notes"
              description="Implementation hints"
              delay={0.7}
            />
            <FeatureCard
              icon={ClipboardList}
              title="Definition of Done"
              description="Complete checklist"
              delay={0.8}
            />
            <FeatureCard
              icon={Scale}
              title="Story Points"
              description="Fibonacci estimation"
              delay={0.9}
            />
            <FeatureCard
              icon={Sparkles}
              title="AI Powered"
              description="Claude Sonnet refinement"
              delay={1.0}
            />
          </motion.div>
        </div>

        {/* Output Section */}
        <AnimatePresence>
          {output && (
            <motion.div
              ref={outputRef}
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 20 }}
              transition={{ duration: 0.5 }}
              className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pb-16"
            >
              <div className="glass rounded-2xl overflow-hidden glow-cyan">
                {/* Output Header */}
                <div className="flex items-center justify-between px-6 py-4 border-b border-white/5">
                  <div className="flex items-center gap-3">
                    <div className="flex gap-1.5">
                      <div className="w-3 h-3 rounded-full bg-red-500/80" />
                      <div className="w-3 h-3 rounded-full bg-yellow-500/80" />
                      <div className="w-3 h-3 rounded-full bg-green-500/80" />
                    </div>
                    <span className="text-sm font-medium text-gray-400">
                      Refined Work Item
                    </span>
                  </div>
                  <div className="flex gap-2">
                    <motion.button
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                      onClick={handleCopy}
                      className="p-2 rounded-lg hover:bg-white/5 transition-colors"
                      title="Copy to clipboard"
                    >
                      {copied ? (
                        <Check className="w-4 h-4 text-green-400" />
                      ) : (
                        <Copy className="w-4 h-4 text-gray-400" />
                      )}
                    </motion.button>
                    <motion.button
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                      onClick={handleDownload}
                      className="p-2 rounded-lg hover:bg-white/5 transition-colors"
                      title="Download as Markdown"
                    >
                      <Download className="w-4 h-4 text-gray-400" />
                    </motion.button>
                  </div>
                </div>

                {/* Output Content */}
                <div className="p-6 sm:p-8 markdown-content">
                  <ReactMarkdown>{output}</ReactMarkdown>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Loading State */}
        <AnimatePresence>
          {isLoading && !output && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pb-16"
            >
              <div className="glass rounded-2xl p-8">
                <div className="flex flex-col items-center justify-center space-y-4">
                  <div className="relative">
                    <div className="w-16 h-16 rounded-full border-4 border-violet-500/20 border-t-violet-500 animate-spin" />
                    <Sparkles className="w-6 h-6 text-violet-400 absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2" />
                  </div>
                  <div className="text-center">
                    <p className="text-white font-medium">Refining your work item...</p>
                    <p className="text-sm text-gray-400 mt-1">
                      Crafting the perfect agile description
                    </p>
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Footer */}
        <footer className="text-center py-8 text-gray-500 text-sm">
          <p>
            Built with{" "}
            <span className="text-violet-400">Next.js</span> &{" "}
            <span className="text-cyan-400">Claude AI</span>
          </p>
        </footer>
      </div>
    </main>
  );
}
