import Layout from "@/components/Shared/Layout";
import {Heading} from "@chakra-ui/react";
import dynamic from "next/dynamic";


const DynamicCartData = dynamic(() =>
        import('@/components/App/Cart').then((module) => module.CartData),
    {
        ssr: false,
    }
);


const Cart = () => {
    const breadcrumbs = [
        {title: 'Кошик'},
    ]
    return <Layout title={''} description={''} breadcrumbs={breadcrumbs}>
        <DynamicCartData/>
    </Layout>
}


export default Cart