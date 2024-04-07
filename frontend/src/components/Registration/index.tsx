import React, { type FC } from 'react';
import Modal from 'react-modal';

import styles from './Registration.module.scss';
import Button from '../../Pages/Track/components/Button';

Modal.setAppElement('#root');

interface RegistrationProps {
	onClick: () => void;
	isOpen: boolean;
	onClose: () => void;
}

const Registration: FC<RegistrationProps> = ({ isOpen = false, onClose, onClick }) => {
	return (
		<Modal
			isOpen={isOpen}
			onRequestClose={onClose}
			overlayClassName={styles.overlay}
			className={styles.modal}
		>
			<Button onClick={onClick} text="Зарегистрироваться" />
		</Modal>
	);
};

export default Registration;
