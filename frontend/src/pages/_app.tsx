import {useEffect} from 'react'
import type {AppProps} from 'next/app'
import {ChakraProvider} from '@chakra-ui/react'
import theme from "@/theme";
import {CartProvider} from "@/context/Cart";

export default function App({Component, pageProps}: AppProps) {
    useEffect(() => {
        const jssStyles = document.querySelector('#jss-server-side');
        if (jssStyles) {
            jssStyles.parentElement?.removeChild(jssStyles);
        }

    }, []);

    return <ChakraProvider theme={theme}>
        <CartProvider>
            <Component {...pageProps} />
        </CartProvider>
    </ChakraProvider>
}