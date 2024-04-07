import React, { type FC } from 'react';

import HumanWalk from '@media/human_walk.svg?react';

import styles from './Icon.module.scss';

const Icon: FC = () => {
	return (
		<div className={styles.root}>
			<div className={styles.container}>
				<HumanWalk className={styles.icon} />
			</div>
		</div>
	);
};

export default Icon;
