'use client';

import Link from 'next/link';
import { ThemeToggle } from '@/components/ThemeToggle';
import { Footer } from '@/components/Footer';
import { ArrowRight, Sparkles, Brain, Zap, Globe, Share2 } from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="flex min-h-screen w-full flex-col bg-white dark:bg-black font-sans text-stone-900 dark:text-stone-100 overflow-x-hidden selection:bg-stone-200 dark:selection:bg-stone-800">

      {/* Navigation */}
      <header className="h-20 flex-none flex items-center px-6 sm:px-8 max-w-7xl mx-auto w-full z-20">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 flex items-center justify-center text-stone-900 dark:text-white">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="w-8 h-8"
            >
              <circle cx="12" cy="12" r="10" />
              <path d="M12 16v-4" />
              <path d="M12 8h.01" />
            </svg>
          </div>
          <h1 className="font-bold text-xl tracking-tighter text-stone-900 dark:text-white">
            ResearchAgent
          </h1>
        </div>
        <div className="flex items-center gap-6 ml-auto">
          <nav className="hidden sm:flex items-center gap-8 text-sm font-medium text-stone-600 dark:text-stone-400">
            <Link href="#features" className="hover:text-stone-900 dark:hover:text-white transition-colors">Features</Link>
            <Link href="#how-it-works" className="hover:text-stone-900 dark:hover:text-white transition-colors">How it works</Link>
            <Link href="https://github.com/SwayamSat/A-Multi-Agent-Research-Assistant-Using-AutoGen" target="_blank" className="hover:text-stone-900 dark:hover:text-white transition-colors">GitHub</Link>
          </nav>
          <div className="h-6 w-px bg-stone-200 dark:bg-stone-800 hidden sm:block"></div>
          <ThemeToggle />
          <Link
            href="/research"
            className="hidden sm:flex items-center gap-2 px-5 py-2.5 rounded-full bg-stone-900 dark:bg-white text-white dark:text-black font-medium text-sm hover:opacity-90 transition-opacity active:scale-95"
          >
            Launch App
          </Link>
        </div>
      </header>

      <main className="flex-1 w-full max-w-7xl mx-auto px-6 sm:px-8 flex flex-col">

        {/* Hero Section */}
        <section className="flex-1 flex flex-col items-center justify-center text-center py-24 sm:py-32 space-y-8 animate-in fade-in zoom-in duration-700 slide-in-from-bottom-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-stone-100 dark:bg-stone-900 border border-stone-200 dark:border-stone-800 text-xs font-semibold uppercase tracking-widest text-stone-500 dark:text-stone-400">
            <Sparkles size={12} className="text-amber-500" />
            <span>v1.0 Now Available</span>
          </div>

          <h1 className="text-5xl sm:text-7xl md:text-8xl font-black tracking-tighter text-stone-900 dark:text-white max-w-4xl mx-auto leading-[0.9]">
            Deep research <br className="hidden sm:block" />
            <span className="text-stone-400 dark:text-stone-600">made autonomous.</span>
          </h1>

          <p className="text-lg sm:text-xl text-stone-600 dark:text-stone-400 max-w-2xl mx-auto leading-relaxed">
            Deploy a squad of AI agents to research any topic, analyze documents, and generate comprehensive reports in minutes, not hours.
          </p>

          <div className="flex flex-col sm:flex-row items-center gap-4 pt-4">
            <Link
              href="/research"
              className="flex items-center gap-3 px-8 py-4 rounded-full bg-stone-900 dark:bg-white text-white dark:text-black font-semibold text-lg hover:opacity-90 transition-all hover:scale-105 active:scale-95 shadow-xl shadow-stone-200/50 dark:shadow-none"
            >
              Start Researching <ArrowRight size={20} />
            </Link>
            <Link
              href="https://github.com/SwayamSat/A-Multi-Agent-Research-Assistant-Using-AutoGen"
              target="_blank"
              className="flex items-center gap-3 px-8 py-4 rounded-full bg-white dark:bg-black border border-stone-200 dark:border-stone-800 text-stone-900 dark:text-white font-medium text-lg hover:bg-stone-50 dark:hover:bg-stone-900 transition-all active:scale-95"
            >
              View on GitHub
            </Link>
          </div>

          {/* Abstract UI Visual */}
          <div className="w-full max-w-5xl mt-16 sm:mt-24 relative group">
            <div className="absolute -inset-1 bg-gradient-to-r from-stone-200 to-stone-400 dark:from-stone-800 dark:to-stone-600 rounded-2xl blur opacity-25 group-hover:opacity-50 transition duration-1000"></div>
            <div className="relative aspect-[16/9] sm:aspect-[21/9] bg-stone-50 dark:bg-stone-900/50 rounded-xl border border-stone-200 dark:border-stone-800 overflow-hidden flex flex-col shadow-2xl">
              {/* Mock Browser/App Header */}
              <div className="h-10 border-b border-stone-200 dark:border-stone-800 flex items-center px-4 gap-2 bg-white/50 dark:bg-black/50 backdrop-blur-sm">
                <div className="flex gap-1.5">
                  <div className="w-3 h-3 rounded-full bg-stone-200 dark:bg-stone-700"></div>
                  <div className="w-3 h-3 rounded-full bg-stone-200 dark:bg-stone-700"></div>
                  <div className="w-3 h-3 rounded-full bg-stone-200 dark:bg-stone-700"></div>
                </div>
              </div>
              {/* Mock Content */}
              <div className="flex-1 p-6 sm:p-10 flex flex-col items-center justify-center text-stone-300 dark:text-stone-700 space-y-4">
                <Brain size={64} className="opacity-20 animate-pulse" />
                <div className="text-sm font-mono opacity-50">Initializing Multi-Agent System...</div>
                <div className="flex gap-2">
                  <span className="w-16 h-2 bg-current rounded-full opacity-20"></span>
                  <span className="w-24 h-2 bg-current rounded-full opacity-20"></span>
                  <span className="w-12 h-2 bg-current rounded-full opacity-20"></span>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Features Grid */}
        <section id="features" className="py-24 border-t border-stone-100 dark:border-stone-900">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <FeatureCard
              icon={<Brain size={24} />}
              title="Autonomous Agents"
              description="Specialized agents collaborate to find, read, and synthesize information autonomously."
            />
            <FeatureCard
              icon={<Globe size={24} />}
              title="Deep Web Search"
              description="Scours the internet for the latest and most relevant papers, articles, and documentation."
            />
            <FeatureCard
              icon={<Share2 size={24} />}
              title="Structured Reports"
              description="Synthesizes findings into comprehensive, readable markdown reports ready for use."
            />
          </div>
        </section>

      </main>

      <Footer />
    </div>
  );
}

function FeatureCard({ icon, title, description }) {
  return (
    <div className="p-8 rounded-3xl bg-stone-50 dark:bg-stone-900/30 border border-stone-100 dark:border-stone-800/50 hover:border-stone-200 dark:hover:border-stone-700 transition-colors group">
      <div className="w-12 h-12 rounded-2xl bg-white dark:bg-stone-800 flex items-center justify-center text-stone-900 dark:text-white mb-6 shadow-sm border border-stone-100 dark:border-stone-700 group-hover:scale-110 transition-transform duration-300">
        {icon}
      </div>
      <h3 className="text-xl font-bold text-stone-900 dark:text-white mb-3">{title}</h3>
      <p className="text-stone-500 dark:text-stone-400 leading-relaxed">
        {description}
      </p>
    </div>
  );
}
