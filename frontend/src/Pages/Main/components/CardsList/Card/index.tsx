import React, { type FC } from 'react';
import { type EventCardType } from '../../../../../models/frontend';

import CoinsIcon from '@media/coins_icon.svg?react';
import AddressIcon from '@media/address_icon.svg?react';
import CuisineIcon from '@media/cuisine_icon.svg?react';

import cn from 'classnames';

import styles from './Card.module.scss';
import { useNavigate } from 'react-router-dom';

export type CardProps = {
	size: 'm' | 's';
	isGigachatCard?: boolean;
} & EventCardType;

const Card: FC<CardProps> = ({
	size,
	imgLink,
	name,
	link,
	address,
	price,
	isGigachatCard = false,
	restaurantType,
}) => {
	const navigate = useNavigate();

	const isSmall = size === 's';

	const handleCardClick = (): void => {
		if (isGigachatCard) {
			navigate('/track');
		} else {
			window.open(link, '_blank');
		}
	};

	return (
		<div
			className={cn(styles.root, {
				[styles.root__small]: isSmall,
			})}
		>
			{isGigachatCard && <div className={styles.tooltip}>Сгенерировано ИИ</div>}
			<img
				className={cn(styles.image, {
					[styles.image__small]: isSmall,
				})}
				src={imgLink}
				alt="image"
			/>
			<div className={cn(styles.info, { [styles.info__small]: isSmall })}>
				<div
					className={cn(styles.title, {
						[styles.title__small]: isSmall,
					})}
				>
					{name}
				</div>
				{isSmall && (
					<>
						{address && (
							<div className={styles.price}>
								<AddressIcon className={styles.price__icon} />
								<div className={styles.price__title}>{address}</div>
							</div>
						)}
						{price && parseInt(price) > 0 && (
							<div className={styles.price}>
								<CoinsIcon className={styles.price__icon} />
								<div className={styles.price__title}>{`Средний чек ${price}₽`}</div>
							</div>
						)}
						{restaurantType && restaurantType.length > 0 && (
							<div key={i} className={styles.price}>
								<CuisineIcon className={styles.price__icon} />
								<div className={styles.price__title}>
									{restaurantType.map((type) => type)}
								</div>
							</div>
						)}
						{restaurantType &&
							restaurantType?.length > 0 &&
							restaurantType.map((type, i) => (
								<div key={i} className={styles.price}>
									<CuisineIcon className={styles.price__icon} />
									<div className={styles.price__title}>{`Средний чек ${price}₽`}</div>
								</div>
							))}
					</>
				)}
				{isGigachatCard && !isSmall && (
					<div className={styles.description}>
						Нейросеть GigaChat построила для вас маршрут на выходные
					</div>
				)}
				<button
					className={cn(styles.button, {
						[styles.button__green]: isGigachatCard,
						[styles.button__small]: isSmall,
					})}
					onClick={handleCardClick}
				>
					Посмотреть
				</button>
			</div>
		</div>
	);
};

export default Card;
