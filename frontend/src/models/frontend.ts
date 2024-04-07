import { type EventType } from '../types';

export interface EventCardType {
	id: string;
	type: EventType;
	name: string;
	link: string;
	restaurantType?: string[];
	reviews?: string[];
	description?: string;
	imgLink?: string;
	price?: string;
	address?: string;
	lat?: number;
	lng?: number;
	time?: number;
	distance?: number;
}
