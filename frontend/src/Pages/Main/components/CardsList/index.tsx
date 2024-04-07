import React, { useMemo, type FC, memo } from 'react';
import { type EventCardType } from '../../../../models/frontend';
import styles from './CardsList.module.scss';
import Card, { type CardProps } from './Card';

interface CardsListProps {
	events: EventCardType[];
}

const CardsList: FC<CardsListProps> = ({ events }) => {
	const mockedEvent: Array<Omit<CardProps, 'onClick'>> = useMemo(() => {
		const result: Array<Omit<CardProps, 'onClick'>> = [];

		events.forEach((event, i) => {
			if (i === 3) {
				result.push({
					...event,
					isGigachatCard: true,
					size: 'm',
				});
			} else {
				result.push({ ...event, size: 'm' });
			}
		});

		return result;
	}, [events]);

	return (
		<div className={styles.root}>
			{mockedEvent.map((event) => (
				<Card {...event} size="m" key={event.id} />
			))}
		</div>
	);
};

export default memo(CardsList);
