import React, {createContext, ReactNode, useCallback, useContext, useEffect, useState} from 'react';

interface CartItem {
    product: number;
    sku: number;
    qty: number;
    images: string[];
    code: string,
    name: string;
    price: number;
    material?: {
        color?: string;
        material?: string;
    };
    url: string;
}

interface CartContextType {
    cart: CartItem[];
    totalItems: number;
    totalQty: number;
    addItem: (item: CartItem) => void;
    updateItem: (sku: number, qty: number) => void;
    removeItem: (sku: number) => void;
    calculateTotal: () => number;
    calculateTotalQty: () => number;
    clearCart: any
}

const CartContext = createContext<CartContextType | undefined>(undefined);

const CartProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const [cart, setCart] = useState<CartItem[]>([]);

    useEffect(() => {
        const storedCart = localStorage.getItem('cart');
        if (storedCart) {
            setCart(JSON.parse(storedCart));
        }
    }, []);

    const updateLocalStorage = useCallback(() => {
        setCart((prevCart) => {
            localStorage.setItem('cart', JSON.stringify(prevCart));
            return prevCart;
        });
    }, []);

    useEffect(() => {
        updateLocalStorage();
    }, [cart, updateLocalStorage]);

    const addItem = (item: CartItem) => {
        const exist = cart.find(cartItem => cartItem.sku === item.sku)
        if (!exist) {
            setCart((prevCart) => [...prevCart, item]);
        }
    };

    const updateItem = (sku: number, qty: number) => {
        setCart((prevCart) =>
            prevCart.map((item) =>
                item.sku === sku ? { ...item, qty } : item
            )
        );
    };

    const removeItem = (sku: number) => {
        setCart((prevCart) => prevCart.filter((item) => item.sku !== sku));
    };

    const calculateTotal = () => {
        return cart.reduce((total, item) => total + item.price * item.qty, 0);
    }

    const calculateTotalQty = () => {
        return cart.reduce((total, item) => total + item.qty, 0);
    }

    const clearCart = () => {
        setCart([])
    }



    return (
        <CartContext.Provider
            value={{
                cart,
                totalItems: calculateTotal(),
                totalQty: calculateTotalQty(),
                addItem,
                updateItem,
                removeItem,
                calculateTotal,
                calculateTotalQty,
                clearCart
            }}
        >
            {children}
        </CartContext.Provider>
    );
};


const useCart = () => {
    const context = useContext(CartContext);
    if (!context) {
        throw new Error('useCart must be used within a CartProvider');
    }
    return context;
};

export {CartProvider, useCart};
