// src/app/components/Navbar.tsx

"use client";

import Link from 'next/link';
import Image from 'next/image';
import { usePathname } from 'next/navigation';
import styles from './Navbar.module.css';

export function Navbar({ activePath }: { activePath?: string }) {
    const pathname = usePathname();

    const isActive = (href: string) => {
        if (activePath === href) {
            return true;
        }

        if (href === '/') {
            return pathname === '/' || pathname.startsWith('/status/');
        }
        return pathname.startsWith(href);
    };

    return (
        <header className={styles.header}>
            <nav className={styles.nav}>
                <div className={`${styles.logoContainer} flex items-center`}>
                    <Image
                        src="/assets/Logo_Transparent.png"
                        alt="KeyFrame Logo"
                        width={75}
                        height={75}
                    />
                </div>

                <div className={styles.navLinks}>
                    {/* 1. 'Generate' Link */}
                    <Link
                        href="/"
                        className={`${styles.navLink} ${isActive('/') ? styles.activeLink : ''}`}
                    >
                        Generate
                    </Link>

                    {/* 2. 'Community Videos' Link */}
                    <Link
                        href="/feed"
                        className={`${styles.navLink} ${isActive('/feed') ? styles.activeLink : ''}`}
                    >
                        Community Videos
                    </Link>

                    {/* 3. 'Team' Link: */}
                    <Link
                        href="/team"
                        className={`${styles.navLink} ${isActive('/team') ? styles.activeLink : ''}`}
                    >
                        Team
                    </Link>
                </div>
            </nav>
        </header>
    );
}
