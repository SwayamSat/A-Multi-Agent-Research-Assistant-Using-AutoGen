import Link from 'next/link';
import { Github, Linkedin, Mail } from 'lucide-react';

export function Footer() {
    return (
        <footer className="border-t border-stone-100 dark:border-stone-900 bg-white dark:bg-black py-12 px-6">
            <div className="max-w-5xl mx-auto flex flex-col sm:flex-row justify-between items-center gap-6">
                <div className="flex flex-col items-center sm:items-start gap-2">
                    <div className="flex items-center gap-2">
                        <div className="w-6 h-6 flex items-center justify-center text-stone-900 dark:text-white">
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                strokeWidth="2"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                className="w-5 h-5"
                            >
                                <circle cx="12" cy="12" r="10" />
                                <path d="M12 16v-4" />
                                <path d="M12 8h.01" />
                            </svg>
                        </div>
                        <span className="font-medium text-stone-900 dark:text-white tracking-tight">ResearchAgent</span>
                    </div>
                    <p className="text-sm text-stone-500 dark:text-stone-400 text-center sm:text-left max-w-xs">
                        Advanced multi-agent research assistant powered by AutoGen & CrewAI.
                    </p>
                </div>

                <div className="flex items-center gap-6">
                    <Link href="https://github.com/SwayamSat" target="_blank" className="text-stone-400 hover:text-stone-900 dark:hover:text-white transition-colors">
                        <Github size={20} />
                    </Link>
                    <Link href="https://www.linkedin.com/in/swayamsatpathy/" target="_blank" className="text-stone-400 hover:text-stone-900 dark:hover:text-white transition-colors">
                        <Linkedin size={20} />
                    </Link>
                    <Link href="mailto:swayam.satpathy24@gmail.com" className="text-stone-400 hover:text-stone-900 dark:hover:text-white transition-colors">
                        <Mail size={20} />
                    </Link>
                </div>
            </div>
            <div className="max-w-5xl mx-auto mt-12 pt-8 border-t border-stone-100 dark:border-stone-900 flex flex-col sm:flex-row justify-between items-center text-xs text-stone-400 gap-4">
                <p>© 2026 ResearchAgent. All rights reserved.</p>
                <div className="flex gap-6">
                    <Link href="#" className="hover:text-stone-900 dark:hover:text-white transition-colors">Privacy</Link>
                    <Link href="#" className="hover:text-stone-900 dark:hover:text-white transition-colors">Terms</Link>
                </div>
            </div>
        </footer>
    );
}
