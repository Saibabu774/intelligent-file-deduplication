export type FileItem={id:number;original_name:string;mime_type:string|null;extension:string|null;size_bytes:number;status:string;is_protected:boolean;created_at:string;hash_value:string|null};
export type Dashboard={total_files:number;total_storage:number;duplicate_files:number;duplicate_storage:number;potential_savings:number;largest_files:FileItem[];recent_uploads:FileItem[]};
