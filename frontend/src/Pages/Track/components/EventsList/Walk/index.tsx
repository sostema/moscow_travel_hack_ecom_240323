import React, { type FC, useMemo } from 'react';

import styles from './Walk.module.scss';
import { type EventCardType } from '../../../../../models/frontend';
import Icon from './Icon';
import { intervalToDuration } from 'date-fns';

type WalkProps = EventCardType;

const Walk: FC<WalkProps> = ({ time, distance }) => {
	const formattedTime = useMemo(() => {
		if (time) {
			const duration = intervalToDuration({ start: 0, end: time * 1000 });
			return `${duration.hours ? duration.hours + 'ч' : ''} ${duration.minutes ? duration.minutes + 'мин' : ''}`;
		}

		return '';
	}, [time]);

	return (
		<div className={styles.root}>
			<Icon />
			<div className={styles.info}>
				{time && <div className={styles.time}>{formattedTime}</div>}
				{time && distance && <div className={styles.dot} />}
				{distance && <div className={styles.distance}>{`${distance}км`}</div>}
			</div>
		</div>
	);
};

export default Walk;
