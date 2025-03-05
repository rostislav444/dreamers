import axios from 'axios';
import { API_BASE_URL } from "@/local";

// Базовый интерфейс для фильтров
export interface BaseFilters {
    page?: number;
    page_size?: number;
    [key: string]: any;
}

export interface PaginatedData<T> {
    results: T[]
    count: number
}

interface BaseResponse {
    ok: boolean;
    status: number;
}

interface StandardResponse<T = any> extends BaseResponse {
    data: T | null;
}

interface PaginatedResponse<T = any> extends BaseResponse {
    data: {
        results: T[];
        count: number;
        next: string | null;
        previous: string | null;
    };
}

type ApiResponse<T = any, P extends boolean = false> =
    P extends true ? PaginatedResponse<T> : StandardResponse<T>;

export interface FetchWrapper {
    get: <T = any, P extends boolean = false, F extends BaseFilters = BaseFilters>(
        url: string,
        filters?: F,
        paginated?: P
    ) => Promise<ApiResponse<T, P>>;

    post: <T = any>(
        url: string,
        body: any
    ) => Promise<StandardResponse<T>>;

    put: <T = any>(
        url: string,
        body: any
    ) => Promise<StandardResponse<T>>;

    delete: <T = any>(
        url: string
    ) => Promise<StandardResponse<T>>;
}

// Функция для преобразования объекта фильтров в строку запроса
const createQueryString = (filters: BaseFilters): string => {
    const params = new URLSearchParams();

    Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '') {
            if (Array.isArray(value)) {
                value.forEach(v => params.append(key, v.toString()));
            } else {
                params.append(key, value.toString());
            }
        }
    });

    return params.toString();
};

const fetchApi = (
    locale: string | undefined = undefined,
    token: string | undefined = undefined
): FetchWrapper => {
    const baseUrl = API_BASE_URL;

    const request = async <T = any, P extends boolean = false>(
        url: string,
        method: 'get' | 'post' | 'put' | 'delete',
        paginated: P = false as P,
        body?: any,
        filters?: BaseFilters
    ): Promise<ApiResponse<T, P>> => {
        if (!url.startsWith('/')) {
            url = '/' + url;
        }

        // Добавляем query параметры, если есть фильтры
        if (filters && Object.keys(filters).length > 0) {
            const queryString = createQueryString(filters);
            url = `${url}${url.includes('?') ? '&' : '?'}${queryString}`;
        }

        const headers = {
            'Content-Type': 'application/json',
            'Accept-Language': locale || 'uk',
            'Authorization': token ? `Bearer ${token}` : undefined,
        };

        try {
            const response = await axios({
                url: baseUrl + url,
                method,
                headers,
                data: body,
            });

            return {
                ok: response.status >= 200 && response.status < 300,
                status: response.status,
                data: response.data,
            } as ApiResponse<T, P>;
        } catch (error: any) {
            return {
                ok: false,
                status: error?.response?.status || 500,
                data: error?.response?.data || null,
            } as ApiResponse<T, P>;
        }
    };

    const get = <T = any, P extends boolean = false, F extends BaseFilters = BaseFilters>(
        url: string,
        filters?: F,
        paginated?: P
    ): Promise<ApiResponse<T, P>> => request<T, P>(url, 'get', paginated || false as P, undefined, filters);

    const post = <T = any>(
        url: string,
        body: any
    ): Promise<StandardResponse<T>> => request(url, 'post', false, body);

    const put = <T = any>(
        url: string,
        body: any
    ): Promise<StandardResponse<T>> => request(url, 'put', false, body);

    const del = <T = any>(
        url: string
    ): Promise<StandardResponse<T>> => request(url, 'delete', false);

    return { get, post, put, delete: del };
};

export default fetchApi;