import { type EventType } from '../types';

export interface EventDataType {
	id: string;
	type: EventType;
	name: string;
	link: string;
	restaurantType: string | null;
	description: string | null;
	imgLink: string | null;
	reviews: string[] | null;
	price: string | null;
	address: string | null;
	lat: number | null;
	lng: number | null;
	time: number | null;
	distance: number | null;
}

export interface RoutesDataType {
	events: EventDataType[];
	distance: number;
	time: number;
}
