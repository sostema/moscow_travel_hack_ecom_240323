import React, { FC } from 'react';

import styles from './Header.module.scss';

const Header: FC = () => {
    return (
        <header>
            <h1 className={styles.title}>Vite + React + TS</h1>
        </header>
    );
};

export default Header;
