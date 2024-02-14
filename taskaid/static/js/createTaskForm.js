// Reactコンポーネント
class CreateTaskForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            name: '',
            subjectTag: '',
            submissionTarget: ''
        };
    }

    handleInputChange = (event) => {
        const target = event.target;
        const value = target.value;
        const name = target.name;

        this.setState({
            [name]: value
        });
    }

    handleSubmit = (event) => {
        event.preventDefault();
        // Submit処理を追加する
        console.log('Form submitted with state:', this.state);
        // フォームデータをサーバーに送信するためのAjaxリクエストを実装することができます
    }

    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <div>
                    <label>Name:</label>
                    <input type="text" name="name" value={this.state.name} onChange={this.handleInputChange} />
                </div>
                <div>
                    <label>Subject Tag:</label>
                    <input type="text" name="subjectTag" value={this.state.subjectTag} onChange={this.handleInputChange} />
                </div>
                <div>
                    <label>Submission Target:</label>
                    <input type="datetime-local" name="submissionTarget" value={this.state.submissionTarget} onChange={this.handleInputChange} />
                </div>
                <button type="submit">Create Task</button>
            </form>
        );
    }
}

// Reactコンポーネントをレンダリング
ReactDOM.render(
    <CreateTaskForm />,
    document.getElementById('root')
);
