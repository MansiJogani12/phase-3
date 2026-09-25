import { GitHubIcon, LoginIcon, LogoutIcon, CoffeeIcon } from "../components/Iconsfile";
import menuIcon from "../assets/menu-icon.png"
import searchIcon from "../assets/search-icon.png"
import { FaShieldAlt } from 'react-icons/fa';
import { useState } from "react";

export const AppHeader = ({ isAuthenticated, user, onLogout, onLogin, repoUrl, setRepoUrl, oncook }) => {
    const [isOpen, setOpen] = useState(false);
    const [isSearchOpen, setSearchOpen] = useState(false);

    return (
        <>
            <header className="sticky top-0 z-30 bg-white/70 backdrop-blur-xl border-b-2 border-black">
                <div className="w-full px-4 xl:px-8 py-3">
                    <div className="flex flex-wrap justify-between items-center gap-4 lg:gap-6">
                        <a
                            href="/"
                            className="text-2xl sm:text-3xl font-bold tracking-tighter sm:block
                                        font-space-mono text-gray-900
                                        hover:text-amber-600 transition-colors"
                        >
                            GitVision
                        </a>

                        {/* mobile version starts here*/}
                        <div className="lg:hidden flex ">
                            <button
                                className="mr-5"
                                onClick={() => { setSearchOpen(true) }}
                            >
                                <img src={searchIcon} alt="search icon" />
                            </button>

                            <div className={`fixed inset-0 z-50 bg-white/30 flex transition-opacity duration-300 lg:hidden ${isSearchOpen ? "opacity-100 pointer-events-auto" : "opacity-0 pointer-events-none"
                                }`}>
                                <div
                                    className={`bg-white w-screen h-48 p-6 shadow-lg relative transform transition-transform duration-300 ease-in-out ${isSearchOpen ? "translate-y-0" : "-translate-y-full"
                                        }`}>
                                    <button
                                        className="absolute top-4 right-4 text-4xl font-bold hover:text-gray-600 transition-colors"
                                        onClick={() => setSearchOpen(false)}
                                    >
                                        &times;
                                    </button>
                                    <p
                                        className="mt-6 text-lg md:text-xl text-gray-700 max-w-lg mx-auto font-semibold"
                                    >
                                        Enter the GitHub repository link:
                                    </p>
                                    <div className="flex-grow flex mt-6 gap-2">
                                        <input
                                            type="text"
                                            value={repoUrl}
                                            onChange={(e) => setRepoUrl(e.target.value)}
                                            onKeyPress={(e) => e.key === 'Enter' && oncook()}
                                            placeholder="Paste a GitHub repo URL to analyze..."
                                            className="w-full px-4 py-2 border-2 border-black rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500 placeholder-gray-500"
                                            aria-label="Repository URL"
                                        />
                                        <button onClick={() => { oncook(), setSearchOpen(false) }} className="bg-[#F9C79A] text-black font-bold px-6 py-2 border-2 border-black rounded-lg hover:bg-amber-400 transition-colors shadow-[3px_3px_0px_rgba(0,0,0,1)] active:shadow-none active:translate-x-0.5 active:translate-y-0.5 whitespace-nowrap">
                                            cook
                                        </button>
                                    </div>
                                </div>
                            </div>

                            <button
                                className="flex flex-col justify-center items-center"
                                onClick={() => setOpen(true)}
                            >
                                <img src={menuIcon} alt="menu icon" />
                            </button>

                            <div className={`fixed inset-0 z-50 bg-white/30 flex transition-opacity duration-300 lg:hidden ${isOpen ? "opacity-100 pointer-events-auto" : "opacity-0 pointer-events-none"
                                }`}>
                                <div className={`bg-white w-64 h-dvh p-6 shadow-lg relative transform transition-transform duration-300 ease-in-out ${isOpen ? "translate-x-0" : "-translate-x-full"
                                    }`}>
                                    <button
                                        className="absolute top-4 right-4 text-4xl font-bold hover:text-gray-600 transition-colors"
                                        onClick={() => setOpen(false)}
                                    >
                                        &times;
                                    </button>
                                    <div className="lg:hidden flex flex-col items-center gap-6 flex-shrink-0 mt-12">
                                        <div className="flex flex-col items-center">
                                            <a
                                                href="https://github.com/herin7/gitforme"
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                className="flex items-center gap-2 px-3 py-1.5 bg-white border-2 border-black rounded-lg hover:bg-gray-100 transition-colors font-semibold shadow-[3px_3px_0px_rgba(0,0,0,1)] active:shadow-none active:translate-x-0.5 active:translate-y-0.5"
                                            >
                                                <GitHubIcon />
                                                <span className="md:inline">Star on GitHub</span>
                                            </a>
                                        </div>

                                        <div className="flex flex-col items-center">
                                            <a
                                                href="/vulnerability-scan"
                                                className="flex items-center gap-2 px-3 py-1.5 bg-white border-2 border-black rounded-lg hover:bg-gray-100 transition-colors font-semibold shadow-[3px_3px_0px_rgba(0,0,0,1)] active:shadow-none active:translate-x-0.5 active:translate-y-0.5"
                                            >
                                                <FaShieldAlt className="text-amber-500" />
                                                <span className="md:inline">Scanner</span>
                                                <span className="bg-amber-500 text-black text-[10px] px-1 rounded-full animate-pulse">New</span>
                                            </a>
                                        </div>

                                        {isAuthenticated ? (
                                            <>
                                                <span className="font-semibold lg:hidden inline">Hi, {user?.username}!</span>
                                                <button onClick={onLogout} className="flex items-center gap-2 px-3 py-1.5 bg-white border-2 border-black rounded-lg hover:bg-gray-100 transition-colors font-semibold shadow-[3px_3px_0px_rgba(0,0,0,1)] active:shadow-none active:translate-x-0.5 active:translate-y-0.5">
                                                    <LogoutIcon />
                                                    <span className="md:inline">Logout</span>
                                                </button>
                                            </>
                                        ) : (
                                                <button type="button" onClick={onLogin} className="flex items-center gap-2 px-3 py-1.5 bg-white border-2 border-black rounded-lg hover:bg-gray-100 transition-colors font-semibold shadow-[3px_3px_0px_rgba(0,0,0,1)] active:shadow-none active:translate-x-0.5 active:translate-y-0.5">
                                                <LoginIcon />
                                                <span className="md:inline">Login</span>
                                            </button>
                                        )}
                                        <div className="flex flex-col items-center">
                                            <a
                                                href="https://herin.vercel.app"
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                className="flex items-center gap-2 px-3 py-1.5 bg-amber-100 border-2 border-black rounded-lg hover:bg-amber-200 transition-colors font-semibold shadow-[3px_3px_0px_rgba(0,0,0,1)] active:shadow-none active:translate-x-0.5 active:translate-y-0.5"
                                            >
                                                who built this?
                                            </a>
                                        </div>
                                    </div>
                                </div>
                                <div onClick={() => setOpen(false)} />
                            </div>
                        </div>


                        {/* mobile version ends here*/}
                        <div className="hidden lg:flex-grow lg:flex gap-2 min-w-[300px] flex-1 xl:flex-none xl:w-1/3">
                            <input
                                type="text"
                                value={repoUrl}
                                onChange={(e) => setRepoUrl(e.target.value)}
                                onKeyPress={(e) => e.key === 'Enter' && oncook()}
                                placeholder="Paste a GitHub repo URL to analyze..."
                                className="w-full px-4 py-2 border-2 border-black rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500 placeholder-gray-500"
                                aria-label="Repository URL"
                            />
                            
                            <label className="bg-white hover:bg-gray-50 text-black px-4 py-2 rounded-lg font-bold border-2 border-black transition-colors flex items-center gap-2 cursor-pointer shadow-[2px_2px_0px_rgba(0,0,0,1)]">
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" /></svg>
                                ZIP Upload
                                <input type="file" className="hidden" accept=".zip" onChange={(e) => alert('ZIP parsing engine starting (Phase 4 integration pending)')} />
                            </label>

                            <button onClick={oncook} className="bg-[#F9C79A] text-black font-bold px-6 py-2 border-2 border-black rounded-lg hover:bg-amber-400 transition-colors shadow-[3px_3px_0px_rgba(0,0,0,1)] active:shadow-none active:translate-x-0.5 active:translate-y-0.5 whitespace-nowrap">
                                cook
                            </button>
                        </div>

                        <div className="hidden lg:flex lg:flex-wrap lg:items-center lg:justify-end lg:gap-3 w-full xl:w-auto mt-4 xl:mt-0">
                            <a
                                href="https://github.com/herin7/gitforme"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="flex items-center gap-2 px-3 py-1.5 bg-white border-2 border-black rounded-lg hover:bg-gray-100 transition-colors font-semibold shadow-[3px_3px_0px_rgba(0,0,0,1)] active:shadow-none active:translate-x-0.5 active:translate-y-0.5"
                            >
                                <GitHubIcon />
                                <span className="hidden md:inline">Star on GitHub</span>
                            </a>

                            <a
                                href="/vulnerability-scan"
                                className="flex items-center gap-2 px-3 py-1.5 bg-white border-2 border-black rounded-lg hover:bg-gray-100 transition-colors font-semibold shadow-[3px_3px_0px_rgba(0,0,0,1)] active:shadow-none active:translate-x-0.5 active:translate-y-0.5"
                            >
                                <FaShieldAlt className="text-amber-500" />
                                <span className="hidden md:inline">Scanner</span>
                                <span className="bg-amber-500 text-black text-[10px] px-1 rounded-full">New</span>
                            </a>

                            {isAuthenticated ? (
                                <>
                                    <span className="font-semibold hidden lg:inline">Hi, {user?.username}!</span>
                                    <button onClick={onLogout} className="flex items-center gap-2 px-3 py-1.5 bg-white border-2 border-black rounded-lg hover:bg-gray-100 transition-colors font-semibold shadow-[3px_3px_0px_rgba(0,0,0,1)] active:shadow-none active:translate-x-0.5 active:translate-y-0.5">
                                        <LogoutIcon />
                                        <span className="hidden md:inline">Logout</span>
                                    </button>
                                </>
                            ) : (
                                    <button type="button" onClick={onLogin} className="flex items-center gap-2 px-3 py-1.5 bg-white border-2 border-black rounded-lg hover:bg-gray-100 transition-colors font-semibold shadow-[3px_3px_0px_rgba(0,0,0,1)] active:shadow-none active:translate-x-0.5 active:translate-y-0.5">
                                    <LoginIcon />
                                    <span className="hidden md:inline">Login</span>
                                </button>
                            )}
                            <div className="flex flex-col items-center">
                                <a
                                    href="https://herin.vercel.app"
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="flex items-center gap-2 px-3 py-1.5 bg-amber-100 border-2 border-black rounded-lg hover:bg-amber-200 transition-colors font-semibold shadow-[3px_3px_0px_rgba(0,0,0,1)] active:shadow-none active:translate-x-0.5 active:translate-y-0.5"
                                >
                                    who built this?
                                </a>
                            </div>
                            <a
                                href="https://coff.ee/herinsoni3a"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="flex items-center gap-2 px-3 py-1.5 bg-yellow-100 border-2 border-black rounded-lg hover:bg-yellow-200 transition-colors font-semibold shadow-[3px_3px_0px_rgba(0,0,0,1)] active:shadow-none active:translate-x-0.5 active:translate-y-0.5"
                                title="Buy me a coffee"
                            >
                                <CoffeeIcon />
                                <span className="hidden lg:inline">Support</span>
                            </a>
                        </div>
                    </div>
                </div>
            </header>
        </>
    )
};
