import React from 'react'
import { useNotifications } from "../../../hooks/useNotifications";
import { NotificationList } from './components/NotificationList';


const NotificationPage = () => {
    const { notifications } = useNotifications();
    return (
        <>
            <NotificationList/>
            <div>NotificationPage</div>
        </>
    )
}

export default NotificationPage