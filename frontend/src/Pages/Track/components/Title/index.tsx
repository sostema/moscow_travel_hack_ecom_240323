import React, { type FC } from 'react';

import styles from './Title.module.scss';

interface TitleProps {
	text: string;
}

const Title: FC<TitleProps> = ({ text }) => {
	return <div className={styles.root}>{text}</div>;
};

export default Title;
