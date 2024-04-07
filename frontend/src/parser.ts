import { type EventDataType } from './models/backend';
import { type EventCardType } from './models/frontend';

export const parseDataTrack = (data: EventDataType[]): EventCardType[] => {
	return data.map((event) => ({
		id: event.id,
		type: event.type,
		name: event.name,
		link: event.link,
		...(event.reviews != null && { reviews: event.reviews }),
		...(event.restaurantType != null && { restaurantType: event.restaurantType }),
		...(event.description != null && { description: event.description }),
		...(event.imgLink != null && { imgLink: event.imgLink }),
		...(event.price != null && { price: event.price }),
		...(event.address != null && { address: event.address }),
		...(event.lat != null && { lat: event.lat }),
		...(event.lng != null && { lng: event.lng }),
		...(event.time != null && { time: event.time }),
		...(event.distance != null && { distance: event.distance }),
	}));
};
