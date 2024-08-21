import Layout from "@/components/Shared/Layout";
import {Heading, Text} from "@chakra-ui/react";
import {useCart} from "@/context/Cart";
import {useEffect} from "react";


const OrderSuccessful = () => {
    const {clearCart} = useCart()

    useEffect(() => {
        clearCart()
    }, [clearCart]);

    const breadcrumbs = [
        {title: 'Оформлення замовлення'},
        {title: 'Замовлення успішно оформлене'},
    ]
    return <Layout title={'Замовлення успішно оформлене'} description={''} breadcrumbs={breadcrumbs}>
        <Heading fontWeight='500'>Ваше замовлення було успішно оформлене</Heading>
        <Text mt={4}>Дуже скоро ми з Вами звʼяжемося</Text>
    </Layout>
}


export default OrderSuccessful