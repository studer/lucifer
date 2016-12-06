var Grid = window.ReactBootstrap.Grid;
var Row = window.ReactBootstrap.Row;
var Col = window.ReactBootstrap.Col;
var Thumbnail = window.ReactBootstrap.Thumbnail;
var Button = window.ReactBootstrap.Button;
var Input = window.ReactBootstrap.Input;

var Links = React.createClass({
  render: function() {
    var createItem = function(item) {
      return (
        <Col md={3} >
          <Thumbnail src={item.hash + '.png'}>
            <h3>{item.title}</h3>
            <p>{item.date}</p>
            <p>
              <Button bsStyle="primary" href={item.url}>Go</Button>
            </p>
          </Thumbnail>
        </Col>
      );
    };
    return <Row>{this.props.links.map(createItem)}</Row>;
  },
});

var Library = React.createClass({
  getInitialState: function() {
    return {links: []};
  },
  onChange: function(e) {
    this.search(e.target.value);
  },
  search: function(search) {
    this.serverRequest = $.get('/search/'+search, function (result) {
      this.setState({
        links: result
      });
    }.bind(this));
  },
  render: function() {
    return (
        <Grid>
          <Row><Col md={4}><h1>Library</h1></Col></Row>
          <Row><Col md={4}>
          <Input
          type="text"
          placeholder="Enter text"
          label="Search the Library"
          help="Search is based on the title."
          hasFeedback
          ref="input"
          groupClassName="group-class"
          labelClassName="label-class"
          onChange={this.onChange} />
          </Col></Row>
          <Links links={this.state.links}/>
        </Grid>
    );
  }
});

ReactDOM.render(<Library />, document.getElementById('container'));
